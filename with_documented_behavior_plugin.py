# /// script
# requires-python = ">=3.10"
# dependencies = ["alembic==1.20.0", "documented-behavior-plugin"]
#
# [tool.uv.sources]
# documented-behavior-plugin = { path = "documented-behavior-plugin" }
# ///
import alembic

print(f"imported alembic {alembic.__version__}")
