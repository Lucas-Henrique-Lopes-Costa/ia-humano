#!/usr/bin/env python3
"""
Teste da funcionalidade incremental da ferramenta de unificação de fotos.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from photo_merger import merge_photos


def test_incremental():
    """Testa a funcionalidade incremental da ferramenta."""

    # Diretórios
    existing_destination = "/Users/lucashenrique/Projetos/Github/ia-humano/Aula 5/Tarefa 1/fotos_unificadas"
    new_source = "/Users/lucashenrique/Projetos/Github/ia-humano/Aula 5/Tarefa 1/teste_incremental"

    print("🧪 TESTE DE FUNCIONALIDADE INCREMENTAL")
    print("=" * 50)

    # Verifica estado inicial
    initial_count = len(
        [f for f in os.listdir(existing_destination) if f.endswith(".png")]
    )
    new_count = len([f for f in os.listdir(new_source) if f.endswith(".png")])

    print(f"📊 Estado inicial:")
    print(f"   Fotos já unificadas: {initial_count}")
    print(f"   Novas fotos para adicionar: {new_count}")

    # Executa o merge incremental
    print(f"\n🔄 Executando merge incremental...")

    # Primeiro tenta o destino como fonte também para verificar se evita duplicatas
    source_dirs = [new_source, existing_destination]
    temp_destination = existing_destination + "_temp"

    # Executa em modo simulação primeiro
    print("\n🧪 Modo simulação:")
    stats = merge_photos(source_dirs, temp_destination, dry_run=True)

    expected_final = initial_count + new_count - stats["duplicates_removed"]
    print(f"\n📈 Resultado esperado: {expected_final} fotos no total")

    # Remove pasta temporária se existir
    if os.path.exists(temp_destination):
        import shutil

        shutil.rmtree(temp_destination)


if __name__ == "__main__":
    test_incremental()
