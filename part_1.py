import argparse
import logging
from aiopath import AsyncPath
from aioshutil import copyfile
from asyncio import run


def init_argparse():
    parser = argparse.ArgumentParser(prog='Copy by extension')
    parser.add_argument('-s', '--source', type=str, help='Path to search')
    parser.add_argument('-o', '--output', type=str, help='Output path')
    return parser


async def read_folder(source_path: AsyncPath, dest_path: AsyncPath):
    async for p in source_path.iterdir():
        if await p.is_dir():
            await read_folder(p, dest_path)
        else:
            await copy_files(p, dest_path)


async def copy_files(source_path: AsyncPath, output_path: AsyncPath):
    try:
        dest_path = output_path / source_path.suffix
        await dest_path.mkdir(exist_ok=True)
        await copyfile(source_path, dest_path / source_path.name)
    except FileExistsError:
        logging.warning(f'File {source_path} already exists')
    except PermissionError:
        logging.warning(f'Permission denied for {source_path}')
    except Exception as e:
        logging.error(e)


if __name__ == '__main__':
    parser = init_argparse()
    args = parser.parse_args()
    logging.info(args)

    source_path = AsyncPath(args.source)
    output_path = AsyncPath(args.output)

    run(read_folder(source_path, output_path))
