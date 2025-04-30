print(ii)
mround = ii.split('_')[-1]
allfiles = glob.glob(ii+os.sep+'*.tif')
unique_prefixes = sorted(set(os.path.basename(f)[:5] for f in allfiles))

for jjdx, jj in enumerate(unique_prefixes):
    image_filenames = glob.glob(ii+os.sep+jj+'*.tif')

    # Paste each image in the correct position
    for index, filename in enumerate(image_filenames):
        row = index // cols
        col = index % cols
        img = Image.open(filename)
        combined_image.paste(img, (col * width, row * height))

    # Save or display the combined image
    outdir0 = main_folder+os.sep+mround+'_'+jj+'.tif'
    combined_image.save(outdir0)
    # combined_image.show()

    ## combined in png rgb preview

            # ----- Binning -----
    bin_factor = 8  # Change to 4, 8, etc. if needed
    combined_np = np.array(combined_image)
    h, w = combined_np.shape
    h_crop = h - h % bin_factor
    w_crop = w - w % bin_factor
    binned_np = combined_np[:h_crop, :w_crop].reshape(
        h_crop // bin_factor, bin_factor,
        w_crop // bin_factor, bin_factor
    ).mean(axis=(1, 3)).astype(np.uint16)

    # Auto window level: scale between min and max
    p_low, p_high = np.percentile(binned_np, (5, 95))  # 1st to 99th percentile window
    scaled = ((binned_np - p_low) / (p_high - p_low) * 255).clip(0, 255).astype(np.uint8)
    rgb_img = np.stack([scaled]*3, axis=-1)
    outdir1 = main_folder+os.sep+mround+'_'+jj+'.png'
    Image.fromarray(rgb_img).save(outdir1, format='PNG', compress_level=9)