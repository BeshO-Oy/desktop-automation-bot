# How to Add Notepad Icon Template

## Why Use a Template?

Using a template image of the Notepad icon will make detection **much more accurate** and prevent the bot from detecting other icons.

## Method 1: Use the Capture Script (Easiest)

1. **Run the capture script:**
   ```powershell
   python capture_icon_template.py
   ```

2. **Follow the instructions:**
   - Position your mouse over the Notepad icon
   - Press Enter
   - The script will capture the icon automatically

3. **Done!** The template will be saved to `resources/icons/notepad_icon.png`

## Method 2: Manual Screenshot

1. **Take a screenshot of the Notepad icon:**
   - Use Windows Snipping Tool or any screenshot tool
   - Capture just the Notepad icon (not the whole desktop)
   - Make sure the icon is clear and visible

2. **Save the image:**
   - Save it as: `notepad_icon.png`
   - Location: `C:\Users\Bishoy\desktop-automation-botcity\resources\icons\notepad_icon.png`

3. **Tips for best results:**
   - Use PNG format for best quality
   - Capture at the same icon size you're using (small/medium/large)
   - Make sure the icon is not obscured or partially hidden
   - Capture when desktop background is visible (not covered by windows)

## File Structure

```
desktop-automation-botcity/
  resources/
    icons/
      notepad_icon.png  ← Put your icon screenshot here
```

## How It Works

Once you add the template:
1. The bot will first try template matching (most accurate)
2. If template matching fails, it falls back to other methods
3. This gives you the best of both worlds: accuracy + flexibility

## Testing

After adding the template, test it:

```powershell
python test_icon_detection.py
```

You should see: "Found Notepad icon using template matching"

## Troubleshooting

**Template not found?**
- Check the file path: `resources/icons/notepad_icon.png`
- Make sure the file exists and is readable
- Check file permissions

**Still detecting wrong icon?**
- Make sure the template image is clear
- Try capturing a larger region (96x96 pixels)
- Ensure the template matches your current icon size
- Try capturing again with a fresh screenshot

**Template too small/large?**
- Desktop icons can be different sizes
- Try capturing at different zoom levels
- The bot will try to match at multiple scales

## Alternative: Multiple Templates

You can also add templates for different icon sizes:
- `notepad_icon_small.png` (32x32)
- `notepad_icon_medium.png` (48x48)
- `notepad_icon_large.png` (96x96)

The bot will try all of them automatically.
