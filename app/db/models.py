import datetime
import os
from sqlalchemy import ForeignKey, String, BigInteger, text
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from dotenv import load_dotenv #pip install python-dotenv
from typing import Annotated, Optional