from pathlib import Path
import json
import math
import cv2

def crop_videos(
    json_file,
    phase_label,
    video_root=None,
    output_root=None,
    codec="mp4v",
    output_resolution=(1280, 720),
):
    json_path = Path(json_file)
    base_dir = json_path.parent
    video_root = Path(video_root) if video_root else base_dir
    output_root = Path(output_root) if output_root else (base_dir / "cropped_by_phase")

    videos_dir = output_root / "videos"
    ped_dir = output_root / "caption_pedestrian"
    veh_dir = output_root / "caption_vehicle"
    videos_dir.mkdir(parents=True, exist_ok=True)
    ped_dir.mkdir(parents=True, exist_ok=True)
    veh_dir.mkdir(parents=True, exist_ok=True)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    records = [data] if isinstance(data, dict) else data

    written = {
        "videos": [],
        "caption_pedestrian": [],
        "caption_vehicle": [],
    }

    for record in records:
        phases = sorted(record["event_phase"], key=lambda p: float(p["start_time"]))

        target_idx = next(
            i for i, p in enumerate(phases)
            if str(phase_label) in [str(x) for x in p["labels"]]
        )
        target_phase = phases[target_idx]

        t_start = float(target_phase["start_time"])
        t_end = float(target_phase["end_time"])

        if target_idx > 0:
            prev_end = float(phases[target_idx - 1]["end_time"])
            # Ensure no overlap with previous phase
            if prev_end != t_start:
                t_start = prev_end

        caption_pedestrian = target_phase["caption_pedestrian"]
        caption_vehicle = target_phase["caption_vehicle"]

        key = "overhead_videos" if "overhead_videos" in record else "vehicle_views"

        for rel_name in record[key]:
            in_path = Path(rel_name)
            if not in_path.is_absolute():
                in_path = video_root / in_path

            cap = cv2.VideoCapture(str(in_path))
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            start_frame = int(math.floor(t_start * fps + 1e-6))
            end_frame_exclusive = int(math.ceil(t_end * fps - 1e-6))
            start_frame = max(0, min(start_frame, frame_count))
            end_frame_exclusive = max(0, min(end_frame_exclusive, frame_count))

            out_video_path = videos_dir / f"{in_path.stem}_phase{phase_label}.mp4"
            out_ped_path = ped_dir / f"{in_path.stem}_phase{phase_label}.txt"
            out_veh_path = veh_dir / f"{in_path.stem}_phase{phase_label}.txt"

            writer = cv2.VideoWriter(
                str(out_video_path),
                cv2.VideoWriter_fourcc(*codec),
                fps,
                output_resolution,
            )

            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
            current_idx = start_frame

            while current_idx < end_frame_exclusive:
                ok, frame = cap.read()
                if not ok:
                    break
                frame = cv2.resize(frame, output_resolution, interpolation=cv2.INTER_LINEAR)
                writer.write(frame)
                current_idx += 1

            writer.release()
            cap.release()

            with open(out_ped_path, "w", encoding="utf-8") as f:
                f.write(caption_pedestrian)

            with open(out_veh_path, "w", encoding="utf-8") as f:
                f.write(caption_vehicle)

            written["videos"].append(out_video_path)
            written["caption_pedestrian"].append(out_ped_path)
            written["caption_vehicle"].append(out_veh_path)

    return written

if __name__ == "__main__":
    # Example usage:
    crop_videos(
        json_file="/path/to/your/json/file.json",
        phase_label="0",
        video_root="/path/to/your/video/overhead_view",
        output_root="cropped_by_phase",
    )