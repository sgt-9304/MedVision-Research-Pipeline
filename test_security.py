from app.settings import settings
from app.security import safe_data_path
def test_safe_path(tmp_path):
 settings().data_root=tmp_path;inside=tmp_path/"study";inside.mkdir();assert safe_data_path(str(inside))==inside.resolve()
