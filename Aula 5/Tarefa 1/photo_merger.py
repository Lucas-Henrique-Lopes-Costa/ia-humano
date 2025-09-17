import os
import hashlib
import shutil
from pathlib import Path
from typing import Dict, Set, List, Tuple
from collections import defaultdict


def calculate_file_hash(file_path: str) -> str:
    """
    Calcula o hash SHA-256 do conteúdo de um arquivo. Para identificar duplicatas.
    """
    try:
        with open(file_path, "rb") as f:
            file_hash = hashlib.sha256()
            # Lê o arquivo em chunks para economizar memória
            while chunk := f.read(8192):
                file_hash.update(chunk)
            return file_hash.hexdigest()
    except Exception as e:
        raise IOError(f"Erro ao calcular hash do arquivo {file_path}: {e}")


def get_unique_filename(destination_dir: str, filename: str) -> str:
    """
    Gera um nome único para um arquivo em caso de conflito.
    """
    base_name, extension = os.path.splitext(filename)
    counter = 1

    while os.path.exists(os.path.join(destination_dir, filename)):
        filename = f"{base_name}_{counter}{extension}"
        counter += 1

    return filename


def scan_directory_images(
    directory: str, extensions: Set[str] = None
) -> Dict[str, Dict]:
    """
    Escaneia um diretório e coleta informações sobre as imagens.
    """
    if extensions is None:
        extensions = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff"}

    files_info = {}

    if not os.path.exists(directory):
        print(f"⚠️  Diretório não encontrado: {directory}")
        return files_info

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            _, ext = os.path.splitext(file.lower())

            if ext in extensions:
                try:
                    file_hash = calculate_file_hash(file_path)
                    files_info[file_path] = {
                        "filename": file,
                        "hash": file_hash,
                        "size": os.path.getsize(file_path),
                        "directory": directory,
                    }
                except IOError as e:
                    print(f"⚠️  Erro ao processar {file_path}: {e}")

    return files_info


def find_duplicates_and_conflicts(files_info: Dict[str, Dict]) -> Tuple[Dict, Dict]:
    """
    Identifica duplicatas (mesmo conteúdo) e conflitos de nomes.
    """
    # Agrupa arquivos por hash (duplicatas)
    hash_groups = defaultdict(list)
    for file_path, info in files_info.items():
        hash_groups[info["hash"]].append(file_path)

    # Filtra apenas grupos com mais de um arquivo (duplicatas)
    duplicates_by_hash = {
        h: files for h, files in hash_groups.items() if len(files) > 1
    }

    # Agrupa arquivos por nome (conflitos potenciais)
    name_groups = defaultdict(list)
    for file_path, info in files_info.items():
        name_groups[info["filename"]].append(file_path)

    # Verifica conflitos: mesmo nome, mas hash diferente
    conflicts_by_name = {}
    for filename, file_paths in name_groups.items():
        if len(file_paths) > 1:
            # Verifica se têm hashes diferentes
            hashes = {files_info[fp]["hash"] for fp in file_paths}
            if len(hashes) > 1:  # Hashes diferentes = conflito real
                conflicts_by_name[filename] = file_paths

    return duplicates_by_hash, conflicts_by_name


def merge_photos(
    source_directories: List[str], destination_directory: str, dry_run: bool = False
) -> Dict:
    """
    Junta fotos de múltiplas pastas, removendo duplicatas e tratando conflitos.
    """
    print("🔍 Escaneando diretórios...")

    # Coleta informações de todos os arquivos
    all_files_info = {}
    for source_dir in source_directories:
        print(f"   📁 Escaneando: {source_dir}")
        dir_files = scan_directory_images(source_dir)
        all_files_info.update(dir_files)
        print(f"      Encontrados: {len(dir_files)} arquivos")

    print(f"\n📊 Total de arquivos encontrados: {len(all_files_info)}")

    # Identifica duplicatas e conflitos
    print("\n🔍 Analisando duplicatas e conflitos...")
    duplicates_by_hash, conflicts_by_name = find_duplicates_and_conflicts(
        all_files_info
    )

    # Estatísticas
    total_duplicates = sum(len(files) - 1 for files in duplicates_by_hash.values())
    total_conflicts = len(conflicts_by_name)

    print(f"   🔄 Grupos de duplicatas: {len(duplicates_by_hash)}")
    print(f"   📄 Arquivos duplicados: {total_duplicates}")
    print(f"   ⚠️  Conflitos de nomes: {total_conflicts}")

    # Mostra duplicatas encontradas
    # if duplicates_by_hash:
    #     print("\n📋 Duplicatas encontradas (mesmo conteúdo):")
    #     for hash_val, file_paths in duplicates_by_hash.items():
    #         print(f"   Hash {hash_val[:12]}...:")
    #         for fp in file_paths:
    #             filename = all_files_info[fp]["filename"]
    #             directory = all_files_info[fp]["directory"]
    #             print(f"      - {filename} (em {os.path.basename(directory)})")

    # Mostra conflitos encontrados
    if conflicts_by_name:
        print("\n⚠️  Conflitos de nomes encontrados (mesmo nome, conteúdo diferente):")
        for filename, file_paths in conflicts_by_name.items():
            print(f"   {filename}:")
            for fp in file_paths:
                directory = all_files_info[fp]["directory"]
                size = all_files_info[fp]["size"]
                print(f"      - {os.path.basename(directory)} ({size} bytes)")

    if dry_run:
        print("\n🧪 Modo simulação ativado - nenhum arquivo será copiado")
        final_count = len(all_files_info) - total_duplicates
        print(f"\n📊 Resultado esperado: {final_count} arquivos únicos")
        return {
            "total_found": len(all_files_info),
            "duplicates_removed": total_duplicates,
            "conflicts_resolved": total_conflicts,
            "final_count": final_count,
        }

    # Cria diretório de destino se não existir
    os.makedirs(destination_directory, exist_ok=True)

    # Processa arquivos
    print(f"\n📦 Copiando arquivos para: {destination_directory}")

    processed_hashes = set()
    copied_files = 0
    skipped_duplicates = 0
    renamed_files = 0

    for file_path, info in all_files_info.items():
        filename = info["filename"]
        file_hash = info["hash"]

        # Pula duplicatas (já processamos um arquivo com este hash)
        if file_hash in processed_hashes:
            skipped_duplicates += 1
            continue

        # Verifica se precisa renomear devido a conflito
        destination_filename = filename
        destination_path = os.path.join(destination_directory, destination_filename)

        if os.path.exists(destination_path):
            # Verifica se é o mesmo arquivo (mesmo hash)
            try:
                existing_hash = calculate_file_hash(destination_path)
                if existing_hash == file_hash:
                    # Mesmo arquivo, pula
                    processed_hashes.add(file_hash)
                    skipped_duplicates += 1
                    continue
                else:
                    # Arquivo diferente, precisa renomear
                    destination_filename = get_unique_filename(
                        destination_directory, filename
                    )
                    destination_path = os.path.join(
                        destination_directory, destination_filename
                    )
                    renamed_files += 1
                    print(f"   🏷️  Renomeando: {filename} → {destination_filename}")
            except IOError:
                # Se não conseguir ler o arquivo existente, renomeia por segurança
                destination_filename = get_unique_filename(
                    destination_directory, filename
                )
                destination_path = os.path.join(
                    destination_directory, destination_filename
                )
                renamed_files += 1

        # Copia arquivo
        try:
            shutil.copy2(file_path, destination_path)
            processed_hashes.add(file_hash)
            copied_files += 1

            if copied_files % 50 == 0:  # Progress indicator
                print(f"   ✅ Copiados: {copied_files} arquivos...")

        except Exception as e:
            print(f"   ❌ Erro ao copiar {file_path}: {e}")

    # Estatísticas finais
    print(f"\n✅ Processo concluído!")
    print(f"   📁 Arquivos copiados: {copied_files}")
    print(f"   🔄 Duplicatas ignoradas: {skipped_duplicates}")
    print(f"   🏷️  Arquivos renomeados: {renamed_files}")
    print(f"   📊 Total no destino: {copied_files}")

    return {
        "total_found": len(all_files_info),
        "duplicates_removed": skipped_duplicates,
        "conflicts_resolved": renamed_files,
        "final_count": copied_files,
    }


if __name__ == "__main__":
    # Exemplo de uso
    source_dirs = [
        "/Users/lucashenrique/Projetos/Github/ia-humano/Aula 5/Tarefa 1/figuras1",
        "/Users/lucashenrique/Projetos/Github/ia-humano/Aula 5/Tarefa 1/figuras2",
    ]

    destination_dir = "/Users/lucashenrique/Projetos/Github/ia-humano/Aula 5/Tarefa 1/fotos_unificadas"

    print("🚀 Ferramenta de Unificação de Fotos")
    print("=" * 50)

    # Primeiro executa em modo simulação
    print("\n🧪 MODO SIMULAÇÃO")
    print("-" * 30)
    stats = merge_photos(source_dirs, destination_dir, dry_run=True)

    # Pergunta se deve prosseguir
    print(f"\n❓ Deseja prosseguir com a cópia real?")
    print(f"   Serão copiados {stats['final_count']} arquivos únicos")

    # Para este exemplo, vamos prosseguir automaticamente
    print("\n🔄 EXECUTANDO CÓPIA REAL")
    print("-" * 30)
    final_stats = merge_photos(source_dirs, destination_dir, dry_run=False)
