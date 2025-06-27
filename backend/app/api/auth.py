from fastapi import APIRouter

router = APIRouter()

@router.post("/login")
async def login():
    """Basic auth endpoint - to be implemented"""
    return {"message": "Auth not implemented yet"}

@router.post("/register")
async def register():
    """Basic registration endpoint - to be implemented"""
    return {"message": "Registration not implemented yet"}

@router.get("/health")
async def auth_health():
    """Health check for auth service"""
    return {"status": "healthy", "service": "auth"}