class User(Base):
    id: int
    username: str
    password_hash: str
    role: str  # 'admin' или 'operator'
    is_active: bool
