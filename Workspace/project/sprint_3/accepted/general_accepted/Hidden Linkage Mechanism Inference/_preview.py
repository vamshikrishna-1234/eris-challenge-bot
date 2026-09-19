import time
from pathlib import Path
from PIL import Image
import generate as g

out = Path("_preview"); out.mkdir(exist_ok=True)
for base_idx in [1, 2]:  # tree, star
    sc = g._sample_scene(g._rng(31, base_idx), base_idx)
    print(f"base {base_idx}: fam={sc['family']} K={sc['K']} ids={sc['ids']}")
    print("   edges:", sc["edges_ids"])
    print("   moving_at_end:", sorted(sc["moving_end"]), " first_mover:", sc["first_mover"])
    t0 = time.time()
    frames = g._render_clip(sc, sc["style_key"], False, g.W_DEFAULT, g.H_DEFAULT)
    print(f"   {len(frames)} frames in {time.time()-t0:.2f}s")
    for fi in [6, 30, 60, 95]:
        Image.fromarray(frames[fi]).save(out / f"b{base_idx}_f{fi:02d}.png")
mframes = g._render_clip(sc, sc["style_key"], True, g.W_DEFAULT, g.H_DEFAULT)
Image.fromarray(mframes[60]).save(out / "mirror_f60.png")
g._encode_mp4(str(out / "sample.mp4"), frames, g.FPS)
print("size KB:", round((out/'sample.mp4').stat().st_size/1024,1))
print("done", out.resolve())
