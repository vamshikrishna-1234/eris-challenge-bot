"""Quick visual preview: render a few scenes, save a frame strip + GT overlay."""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
import generate as gen

OUT = Path("_preview"); OUT.mkdir(exist_ok=True)
marg = 26
scale = (gen.W_DEFAULT - 2 * marg) / gen.GRID

for base_idx in range(4):
    rng = gen._rng(7, base_idx)
    scene = gen._sample_scene(rng, base_idx)
    sim = gen._simulate_scene(scene)
    frames = gen._render_clip(scene, sim, scene["style_key"], scale, marg,
                              gen.W_DEFAULT, gen.H_DEFAULT)
    picks = [15, 40, 65, gen.N_FRAMES - 1]
    strip = np.concatenate([frames[p] for p in picks], axis=1)
    Image.fromarray(strip).save(OUT / f"{base_idx}_{scene['family']}_solver.png")

    # ground-truth overlay on the last frame (shade hidden block cells)
    gt = Image.fromarray(frames[-1]).copy()
    d = ImageDraw.Draw(gt)
    for (c, ry) in scene["occ"]:
        x0, y0 = gen._board_to_px(c, ry + 1, scale, marg)
        x1, y1 = gen._board_to_px(c + 1, ry, scale, marg)
        d.rectangle([x0, y0, x1, y1], outline=(150, 50, 30), width=3)
    gt.save(OUT / f"{base_idx}_{scene['family']}_truth.png")
    print(f"{base_idx}: {scene['family']:8s} probes={scene['num_probes']} "
          f"n_obs={sim['n_obstacles']} query_col={scene['query_col']} "
          f"hit_row={sim['query_hit_row']} occ_cells={sim['occupancy'].count('1')}")
print("saved previews to _preview/")
