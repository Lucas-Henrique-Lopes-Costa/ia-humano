#!/usr/bin/env python3
"""
Exemplo completo de uso da ferramenta de unificação de fotos.

Este script demonstra como usar a ferramenta para:
1. Unificar fotos de múltiplas pastas
2. Executar de forma incremental
3. Usar diferentes configurações

Uso:
    python exemplo_uso.py
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from photo_merger import (
    merge_photos,
    scan_directory_images,
    find_duplicates_and_conflicts,
)


def exemplo_basico():
    """Exemplo básico de unificação de duas pastas."""
    print("🔥 EXEMPLO 1: Unificação Básica")
    print("=" * 50)

    source_dirs = [
        "/Users/lucashenrique/Projetos/Github/ia-humano/Aula 5/Tarefa 1/figuras1",
        "/Users/lucashenrique/Projetos/Github/ia-humano/Aula 5/Tarefa 1/figuras2",
    ]

    destination_dir = "/Users/lucashenrique/Projetos/Github/ia-humano/Aula 5/Tarefa 1/exemplo_unificacao"

    print(f"📁 Pastas de origem:")
    for i, source in enumerate(source_dirs, 1):
        print(f"   {i}. {os.path.basename(source)}")

    print(f"📁 Pasta de destino: {os.path.basename(destination_dir)}")

    # Executa em modo simulação
    print(f"\n🧪 Executando em modo simulação...")
    stats = merge_photos(source_dirs, destination_dir, dry_run=True)

    print(f"\n📊 Resumo:")
    print(f"   • Arquivos encontrados: {stats['total_found']}")
    print(f"   • Duplicatas removidas: {stats['duplicates_removed']}")
    print(f"   • Conflitos resolvidos: {stats['conflicts_resolved']}")
    print(f"   • Arquivos únicos finais: {stats['final_count']}")


def exemplo_analise_detalhada():
    """Exemplo de análise detalhada sem realizar cópias."""
    print("\n\n🔍 EXEMPLO 2: Análise Detalhada")
    print("=" * 50)

    # Escaneia apenas para análise
    print("📊 Analisando conteúdo das pastas...")

    figuras1_info = scan_directory_images(
        "/Users/lucashenrique/Projetos/Github/ia-humano/Aula 5/Tarefa 1/figuras1"
    )
    figuras2_info = scan_directory_images(
        "/Users/lucashenrique/Projetos/Github/ia-humano/Aula 5/Tarefa 1/figuras2"
    )

    all_files = {**figuras1_info, **figuras2_info}

    print(f"   📁 figuras1: {len(figuras1_info)} arquivos")
    print(f"   📁 figuras2: {len(figuras2_info)} arquivos")
    print(f"   📊 Total: {len(all_files)} arquivos")

    # Encontra duplicatas e conflitos
    duplicates, conflicts = find_duplicates_and_conflicts(all_files)

    print(f"\n🔍 Análise de duplicatas:")
    print(f"   🔄 Grupos de duplicatas: {len(duplicates)}")

    total_duplicates = sum(len(files) - 1 for files in duplicates.values())
    print(f"   📄 Arquivos duplicados: {total_duplicates}")

    print(f"\n⚠️  Análise de conflitos:")
    print(f"   🏷️  Conflitos de nomes: {len(conflicts)}")

    if conflicts:
        for filename, paths in conflicts.items():
            print(f"   • {filename}:")
            for path in paths:
                info = all_files[path]
                folder = os.path.basename(info["directory"])
                print(f"     - {folder}: {info['size']} bytes")

    unique_files = len(all_files) - total_duplicates
    print(f"\n✨ Resultado final esperado: {unique_files} arquivos únicos")


def exemplo_uso_real():
    """Exemplo de como usar em cenário real."""
    print("\n\n📱 EXEMPLO 3: Cenário Real")
    print("=" * 50)

    print("💡 Em um cenário real, você usaria assim:")
    print()
    print("1️⃣  Para unificar fotos de várias pessoas:")
    print("   source_dirs = [")
    print("       '/caminho/para/fotos_joao',")
    print("       '/caminho/para/fotos_maria',")
    print("       '/caminho/para/fotos_pedro'")
    print("   ]")
    print("   destination = '/caminho/para/fotos_familia'")
    print()
    print("2️⃣  Para adicionar fotos novas sem duplicar:")
    print("   source_dirs = [")
    print("       '/caminho/para/novas_fotos',")
    print("       '/caminho/para/fotos_familia'  # <- pasta existente")
    print("   ]")
    print("   destination = '/caminho/para/fotos_familia_temp'")
    print("   # depois mover de _temp para fotos_familia")
    print()
    print("3️⃣  Para verificar antes de fazer alterações:")
    print("   merge_photos(source_dirs, destination, dry_run=True)")
    print()
    print("🎯 Funcionalidades principais:")
    print("   ✅ Detecta duplicatas por conteúdo (não apenas nome)")
    print("   ✅ Preserva arquivos diferentes com mesmo nome")
    print("   ✅ Funciona com qualquer quantidade de pastas")
    print("   ✅ Modo simulação para verificar antes de executar")
    print("   ✅ Logs detalhados do processo")
    print("   ✅ Suporte a múltiplos formatos de imagem")


if __name__ == "__main__":
    print("🚀 FERRAMENTA DE UNIFICAÇÃO DE FOTOS")
    print("🔧 Exemplos de Uso e Funcionalidades")
    print("=" * 60)

    try:
        exemplo_basico()
        exemplo_analise_detalhada()
        exemplo_uso_real()

        print("\n\n✅ Todos os exemplos executados com sucesso!")
        print("📚 Consulte o arquivo photo_merger.py para ver o código completo.")

    except Exception as e:
        print(f"\n❌ Erro durante a execução: {e}")
        sys.exit(1)
