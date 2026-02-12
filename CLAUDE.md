# CLAUDE.md - Project Steering Guide

## 1. Project Overview

`spec-Workflow-mcp` を核とした仕様駆動開発（SDD）プロジェクト。

- **目的**: ユーザーとの対話を通じ、仕様から実装までを一貫して管理・構築する。
- **言語環境**: 日本語（コミュニケーション、ドキュメント、Issue、コミットメッセージ）。

## 2. Core Workflow: spec-Workflow-mcp

本プロジェクトは、以下の MCP 標準ワークフローを厳格に遵守する。

1. **Specification Phase**:
    - MCP を通じて仕様を定義・更新する。
2. **Task Definition Phase**:
    - 仕様に基づき、実行可能な最小単位のタスクリストを作成する。
3. **Approval**:
    - ユーザーからタスクリストの承認を得る。
4. **Execution**:
    - 承認されたタスクを GitHub Issue と紐付けて実行する。

## 3. Implementation & GitHub Management

タスクの実行においては GitHub CLI (`gh`) を活用し、透明性の高い開発を行う。

### Task & Issue Integration

- **Decomposition**: 承認された各タスクに対し、**1つの GitHub Issue** を作成する。
- **Progress Tracking**:
  - **開始**: Issue ステータスを `In Progress` に変更する。
  - **完了**: 実装後の承認を経て、Issue を `Done` に変更する。
- **Workflow**: `gh issue create` -> `gh pr create` -> `gh pr merge` のサイクルを基本とする。

### Code Delivery

- ブランチ運用、プルリクエストの作成、マージ作業はすべて GitHub CLI を用いて自動化・効率化する。
- プルリクエストには必ず関連する Issue 番号を記載する。

## 4. Operational Principles

- **No Assumptions**: 仕様が不明確な場合は、実装を進めず必ず MCP を通じて仕様の具体化を行う。
- **Atomic Commits**: 1つの Issue / PR は、単一の論理的変更のみを含むように管理する。
- **Dynamic Adaptability**: 技術スタックや具体的ツールは、仕様定義のフェーズで決定し、必要に応じて本ガイドを拡張する。
