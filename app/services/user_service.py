from sqlmodel import Session

from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate, UserUpdate, TokenResponse, LoginRequest


class UserService:
    def __init__(self, session: Session):
        self.repo = UserRepository(session)

    def get_all_users(self) -> list[User]:
        return self.repo.get_all()

    def get_user_by_id(self, user_id: int) -> User:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        return user

    def create_user(self, data: UserCreate) -> User:
        existing = self.repo.get_by_email(data.email)
        if existing:
            raise ValueError("E-mail already registered")
        if len(data.password) < 8:
            raise ValueError("Password must be at least 8 characters")
        user = User(
            email=data.email,
            hashed_password=hash_password(data.password),
            full_name=data.full_name,
        )
        return self.repo.create(user)

    def update_user(self, user_id: int, data: UserUpdate) -> User:
        user = self.get_user_by_id(user_id)
        if data.email:
            existing = self.repo.get_by_email(data.email)
            if existing and existing.id != user_id:
                raise ValueError("E-mail already in use")
            user.email = data.email
        if data.full_name:
            user.full_name = data.full_name
        if data.is_active is not None:
            user.is_active = data.is_active
        return self.repo.update(user)

    def delete_user(self, user_id: int) -> None:
        user = self.get_user_by_id(user_id)
        self.repo.delete(user)

    def login(self, data: LoginRequest) -> TokenResponse:
        user = self.repo.get_by_email(data.email)
        if not user or not verify_password(data.password, user.hashed_password):
            raise ValueError("Invalid e-mail or password")
        if not user.is_active:
            raise ValueError("Inactive user")
        token = create_access_token(data={"sub": str(user.id), "role": user.role})
        return TokenResponse(access_token=token)