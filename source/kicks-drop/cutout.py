import sys, numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
im = Image.open(sys.argv[1]).convert("RGB"); a = np.asarray(im).astype(float); R, G, B = a[..., 0], a[..., 1], a[..., 2]
bgm = (R > G * 1.55) & (R > B * 1.45) & (R > 45)            # saturated red satin and its shadows
shoe = ~bgm
shoe = ndimage.binary_opening(shoe, iterations=2)
lab, n = ndimage.label(shoe); sizes = ndimage.sum(shoe, lab, range(1, n + 1)); keep = np.argsort(sizes)[::-1][:1] + 1
shoe = np.isin(lab, keep)
# fill small holes only (keep the real gaps between the laces and the two shoes)
holes = ndimage.binary_fill_holes(shoe) & ~shoe; hl, hn = ndimage.label(holes); hs = ndimage.sum(holes, hl, range(1, hn + 1))
small = np.isin(hl, np.where(hs < 4000)[0] + 1); shoe = shoe | small
alpha = Image.fromarray((shoe * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
# de-spill: pull red cast out of the edge pixels
spill = np.clip((R - (G + B) / 2) / 255, 0, 1)[..., None]; fixed = a.copy(); fixed[..., 0] = np.minimum(R, (G + B) / 2 + 12)
edge = np.asarray(alpha.filter(ImageFilter.MaxFilter(9))).astype(float) - np.asarray(alpha.filter(ImageFilter.MinFilter(9))).astype(float)
w = (edge / 255)[..., None]; rgb = fixed * w + a * (1 - w)
out = Image.fromarray(np.dstack([rgb, np.asarray(alpha)]).astype(np.uint8), "RGBA"); bbox = out.getbbox(); out = out.crop(bbox)
out.save(sys.argv[2]); print("bbox", bbox, "size", out.size)
prev = Image.new("RGBA", out.size, (17, 17, 17, 255)); prev.alpha_composite(out); prev.convert("RGB").resize((out.size[0] // 2, out.size[1] // 2)).save(sys.argv[3])
