import os
import sys
import pytest
from httpx import Response
import httpx
import nltk

TEST_ROOT = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(TEST_ROOT, ".."))
sys.path.insert(0, PROJECT_ROOT)

from UrlCompressorApi.services import URLShortenerService, QRCodeService, SlugGeneratorService

class MockTransport(httpx.BaseTransport):
    def __init__(self, html: str):
        self.html = html
    def handle_request(self, request):
        return Response(200, text=self.html)


def test_encode_decode_roundtrip():
    service = URLShortenerService()
    numbers = [1, 10, 62, 12345, 999999]
    for n in numbers:
        code = service.encode(n)
        assert service.decode(code) == n

def test_generate_qr_base64():
    qr_service = QRCodeService()
    data = 'https://example.com'
    qr = qr_service.generate_qr_base64(data)
    assert isinstance(qr, str) and len(qr) > 0

def test_generate_slug(monkeypatch):
    html = '<html><head><title>Example Domain</title></head><body><p>Example description here</p></body></html>'
    transport = MockTransport(html)
    client = httpx.Client(transport=transport)
    monkeypatch.setattr(httpx, 'get', client.get)
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    slug_service = SlugGeneratorService()
    slug = slug_service.generate_slug('http://example.com')
    assert slug
