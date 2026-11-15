import os
from PIL import Image, ImageSequence

def rebuild_gif_from_frames():
    # Supports running from inside ~/lec13 or anywhere else
    base_dir = os.path.dirname(os.path.abspath(__file__))
    source_gif = os.path.join(base_dir, "ffmpeg", "out.gif")
    if not os.path.exists(source_gif):
        source_gif = "/Users/vivekdalmia/lec13/ffmpeg/out.gif"

    frames_dir = os.path.join(base_dir, "frames")
    output_gif = os.path.join(base_dir, "rebuilt_pillow.gif")

    # Step 1: Extract individual frames from yesterday's ffmpeg out.gif
    os.makedirs(frames_dir, exist_ok=True)
    print(f"Opening yesterday's ffmpeg GIF: {source_gif}")

    with Image.open(source_gif) as im:
        duration = im.info.get("duration", 30)
        loop = im.info.get("loop", 0)
        frame_paths = []

        print(f"Extracting frames (size: {im.size}, total: {im.n_frames})...")
        for i, frame in enumerate(ImageSequence.Iterator(im)):
            frame_path = os.path.join(frames_dir, f"frame_{i:02d}.png")
            frame.save(frame_path)
            frame_paths.append(frame_path)

        print(f"Extracted {len(frame_paths)} frames into {frames_dir}/")

    # Step 2: Load the frames from disk and rebuild into a moving GIF with Pillow
    print("Rebuilding moving GIF from extracted frames...")
    loaded_frames = [Image.open(p) for p in sorted(frame_paths)]

    # Pillow requires save_all=True on the first frame, passing remaining frames via append_images
    loaded_frames[0].save(
        output_gif,
        save_all=True,
        append_images=loaded_frames[1:],
        duration=duration,
        loop=loop
    )

    # Clean up open file pointers
    for frame_img in loaded_frames:
        frame_img.close()

    print(f"Successfully rebuilt moving GIF with Pillow: {output_gif}")
    print(f"Original ffmpeg file size: {os.path.getsize(source_gif):,} bytes")
    print(f"Pillow rebuilt file size:  {os.path.getsize(output_gif):,} bytes")

if __name__ == "__main__":
    rebuild_gif_from_frames()
