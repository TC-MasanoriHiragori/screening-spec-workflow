#!/usr/bin/env python3
"""
OpenAPI 仕様書をYAML形式でエクスポートするスクリプト

FastAPIアプリケーションからOpenAPI 3.1仕様を取得し、
YAML形式で openapi.yaml に保存します。
"""

import sys
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.presentation.main import app


def export_openapi_to_yaml(output_path: str = "openapi.yaml") -> None:
    """
    OpenAPI仕様をYAML形式でエクスポート

    Args:
        output_path: 出力ファイルパス（デフォルト: openapi.yaml）
    """
    try:
        import yaml
    except ImportError:
        print("エラー: pyyaml がインストールされていません")
        print("インストール: uv add pyyaml")
        sys.exit(1)

    # OpenAPI仕様を取得
    openapi_schema = app.openapi()

    # プロジェクトルートに出力
    output_file = project_root / output_path

    # YAML形式で保存
    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(
            openapi_schema,
            f,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
        )

    print(f"✅ OpenAPI仕様を {output_file} に保存しました")
    print(f"📄 OpenAPIバージョン: {openapi_schema.get('openapi', 'N/A')}")
    print(f"📋 タイトル: {openapi_schema.get('info', {}).get('title', 'N/A')}")
    print(f"🔢 バージョン: {openapi_schema.get('info', {}).get('version', 'N/A')}")
    print(f"🛣️  エンドポイント数: {len(openapi_schema.get('paths', {}))}")


if __name__ == "__main__":
    export_openapi_to_yaml()
