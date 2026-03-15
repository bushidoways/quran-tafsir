"""
Model dan Skema Data

Definisi model Pydantic untuk validasi request dan response API.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class MufassirEnum(str, Enum):
    """Daftar mufassir (penulis tafsir) yang tersedia dan terverifikasi."""
    IBN_KATHIR = "ibn-kathir"
    AS_SADI = "as-sadi"
    AL_TABARI = "al-tabari"
    AL_BAGHAWI = "al-baghawi"
    IBN_RAJAB = "ibn-rajab"
    AS_SHANQITI = "as-shanqiti"
    IBN_ABI_HATIM = "ibn-abi-hatim"
    IBN_AL_QAYYIM = "ibn-al-qayyim"
    IBN_ABBAS = "ibn-abbas"
    AL_UTHAYMEEN = "al-uthaymeen"


class SearchRequest(BaseModel):
    """Model untuk request pencarian tafsir."""
    query: str = Field(..., min_length=1, max_length=200, description="Kata kunci pencarian")
    mufassir: MufassirEnum = Field(MufassirEnum.IBN_KATHIR, description="Mufassir yang dipilih")
    page: int = Field(1, ge=1, description="Nomor halaman")
    limit: int = Field(10, ge=1, le=50, description="Hasil per halaman")


class TafsirResponse(BaseModel):
    """Model untuk response tafsir."""
    surah: int
    ayah: int
    text_arab: Optional[str] = None
    text_latin: Optional[str] = None
    terjemahan: Optional[str] = None
    tafsir: str
    mufassir: str
    quote: Optional[str] = None


class QuoteResponse(BaseModel):
    """Model untuk response quotes Al-Qur'an."""
    text: str
    surah: str
    ayah: int
    theme: Optional[str] = None


class SurahInfo(BaseModel):
    """Model untuk informasi surah."""
    number: int
    name_arab: str
    name_latin: str
    name_indonesia: Optional[str] = None
    total_ayah: int
    tempat_turun: str
    description: Optional[str] = None
