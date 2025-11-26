import os
import sys

def combine_all_chunks(session_folder, final_dir="data/final_recordings"):
    """
    Scans the session directory, finds all player/round folders,
    combines each round's chunks into a .webm file inside final_recordings/[session]/.
    Output filenames will include session, player, and round info.
    """
    session_part = os.path.basename(session_folder)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    session_outdir = os.path.join(project_root, final_dir, session_part)
    os.makedirs(session_outdir, exist_ok=True)
    '''
    session_part = os.path.basename(session_folder)
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Create main final_recordings/session_xxx folder
    session_outdir = os.path.join(script_dir, final_dir, session_part)
    os.makedirs(session_outdir, exist_ok=True)
    '''

    for player_folder in os.listdir(session_folder):
        player_path = os.path.join(session_folder, player_folder)
        if not os.path.isdir(player_path) or not player_folder.startswith("player_"):
            continue

        for round_folder in os.listdir(player_path):
            round_path = os.path.join(player_path, round_folder)
            if not os.path.isdir(round_path) or not round_folder.startswith("round_"):
                continue

            chunks = sorted([
                f for f in os.listdir(round_path)
                if f.startswith("chunk_") and f.endswith(".webm")
            ])
            if not chunks:
                print(f"No chunks found in {round_path}")
                continue

            outname = f"{session_part}__{player_folder}__{round_folder}.webm"
            outpath = os.path.join(session_outdir, outname)
            print(f"Combining {len(chunks)} chunks for {outname}")

            with open(outpath, "wb") as out:
                for chunk in chunks:
                    chunk_file = os.path.join(round_path, chunk)
                    with open(chunk_file, "rb") as f:
                        out.write(f.read())

    print(f"All files combined! Output directory: {session_outdir}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage:\n  python combine_all_chunks.py /path/to/session_folder")
        sys.exit(1)
    combine_all_chunks(sys.argv[1])