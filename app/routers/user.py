from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_db
from app.models.user import User
from app.models.company import Company
from app.core.auth import create_access_token, get_current_user

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# =========================
# SCHEMAS
# =========================

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    company_name: str
    cnpj: str


# =========================
# CREATE USER + COMPANY
# =========================

@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    # Verifica se email já existe
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )

    # Verifica se CNPJ já existe
    existing_company = db.query(Company).filter(Company.cnpj == user.cnpj).first()
    if existing_company:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CNPJ já cadastrado"
        )

    # Cria empresa
    new_company = Company(
        name=user.company_name,
        cnpj=user.cnpj,
        plan="free"
    )

    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    # Hash da senha
    hashed_password = pwd_context.hash(user.password)

    # Cria usuário vinculado à empresa
    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        company_id=new_company.id,
        is_admin=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email,
        "company": {
            "id": new_company.id,
            "name": new_company.name,
            "plan": new_company.plan
        }
    }


# =========================
# LOGIN (OAuth2 padrão)
# =========================

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.email == form_data.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Credenciais inválidas"
        )

    if not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Credenciais inválidas"
        )

    access_token = create_access_token(
        data={
            "sub": user.email,
            "user_id": user.id,
            "company_id": user.company_id
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# =========================
# ROTA PROTEGIDA
# =========================

@router.get("/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "is_admin": current_user.is_admin,
        "company_id": current_user.company_id
    }