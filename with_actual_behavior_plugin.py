# /// script
# requires-python = ">=3.10"
# dependencies = ["alembic==1.20.0", "actual-behavior-plugin"]
#
# [tool.uv.sources]
# actual-behavior-plugin = { path = "actual-behavior-plugin" }
# ///
import alembic

print(f"imported alembic {alembic.__version__}")
