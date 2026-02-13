#!/usr/bin/env python
"""
OpenAPI仕様書エクスポートスクリプト

このスクリプトは、FastAPIアプリケーションからOpenAPI 3.0仕様を
YAML形式でエクスポートします。

Usage:
    uv run python scripts/export_openapi.py
"""

import sys
from pathlib import Path

import yaml

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.presentation.main import app


def export_openapi_to_yaml(output_path: str = "openapi.yaml") -> None:
    """
    OpenAPI仕様をYAMLファイルにエクスポート

    Args:
        output_path: 出力先のYAMLファイルパス

    Note:
        FastAPIのapp.openapi()メソッドを使用して、
        OpenAPI仕様をJSON形式で取得し、YAML形式に変換します。
    """
    # OpenAPI仕様を取得
    openapi_schema = app.openapi()

    # YAMLファイルに出力
    output_file = Path(project_root) / output_path
    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(
            openapi_schema,
            f,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
        )

    print(f"✓ OpenAPI仕様を {output_file} にエクスポートしました")
    print(f"  - Title: {openapi_schema['info']['title']}")
    print(f"  - Version: {openapi_schema['info']['version']}")
    print(f"  - Endpoints: {len(openapi_schema['paths'])} paths")


def main():
    """メイン関数"""
    try:
        export_openapi_to_yaml()
    except Exception as e:
        print(f"✗ エラーが発生しました: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
