#!/usr/bin/env python3
"""kicad-visual-diff.py — Generate a visual diff of KiCad schematic sheets.

Usage:
    python3 kicad-visual-diff.py \
        --base-dir /tmp/base \
        --head-dir /tmp/head \
        --feature buck-converter-5v \
        --output-dir /tmp/diff-output

Always exits 0. Errors are recorded as warnings, never crashes.
"""

import argparse
import base64
import datetime
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Optional dependency detection
# ---------------------------------------------------------------------------

try:
    from PIL import Image
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

try:
    import cairosvg  # type: ignore
    CAIROSVG_AVAILABLE = True
except ImportError:
    CAIROSVG_AVAILABLE = False

try:
    import numpy as np  # type: ignore
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

# ---------------------------------------------------------------------------
# Embedded panzoom v4.5.1 — MIT licence — https://github.com/timmywil/panzoom
# Source fetched from npm (@panzoom/panzoom@4.5.1/dist/panzoom.min.js)
# ---------------------------------------------------------------------------

_PANZOOM_JS = r"""/**
* Panzoom for panning and zooming elements using CSS transforms
* Copyright Timmy Willison and other contributors
* https://github.com/timmywil/panzoom/blob/main/MIT-License.txt
*/
!function(t,e){"object"==typeof exports&&"undefined"!=typeof module?module.exports=e():"function"==typeof define&&define.amd?define(e):(t="undefined"!=typeof globalThis?globalThis:t||self).Panzoom=e()}(this,function(){"use strict";var Y=function(){return(Y=Object.assign||function(t){for(var e,n=1,o=arguments.length;n<o;n++)for(var r in e=arguments[n])Object.prototype.hasOwnProperty.call(e,r)&&(t[r]=e[r]);return t}).apply(this,arguments)};function C(t,e){for(var n=t.length;n--;)if(t[n].pointerId===e.pointerId)return n;return-1}function T(t,e){if(e.touches)for(var n=0,o=0,r=e.touches;o<r.length;o++){var a=r[o];a.pointerId=n++,T(t,a)}else-1<(n=C(t,e))&&t.splice(n,1),t.push(e)}function N(t){for(var e,n=(t=t.slice(0)).pop();e=t.pop();)n={clientX:(e.clientX-n.clientX)/2+n.clientX,clientY:(e.clientY-n.clientY)/2+n.clientY};return n}function L(t){var e;return t.length<2?0:(e=t[0],t=t[1],Math.sqrt(Math.pow(Math.abs(t.clientX-e.clientX),2)+Math.pow(Math.abs(t.clientY-e.clientY),2)))}"undefined"!=typeof window&&(window.NodeList&&!NodeList.prototype.forEach&&(NodeList.prototype.forEach=Array.prototype.forEach),"function"!=typeof window.CustomEvent&&(window.CustomEvent=function(t,e){e=e||{bubbles:!1,cancelable:!1,detail:null};var n=document.createEvent("CustomEvent");return n.initCustomEvent(t,e.bubbles,e.cancelable,e.detail),n}));var V={down:"mousedown",move:"mousemove",up:"mouseup mouseleave"};function D(t,e,n,o){V[t].split(" ").forEach(function(t){e.addEventListener(t,n,o)})}function G(t,e,n){V[t].split(" ").forEach(function(t){e.removeEventListener(t,n)})}"undefined"!=typeof window&&("function"==typeof window.PointerEvent?V={down:"pointerdown",move:"pointermove",up:"pointerup pointerleave pointercancel"}:"function"==typeof window.TouchEvent&&(V={down:"touchstart",move:"touchmove",up:"touchend touchcancel"}));var a,i="undefined"!=typeof document&&!!document.documentMode;var c=["webkit","moz","ms"],l={};function I(t){if(l[t])return l[t];var e=a=a||document.createElement("div").style;if(t in e)return l[t]=t;for(var n=t[0].toUpperCase()+t.slice(1),o=c.length;o--;){var r="".concat(c[o]).concat(n);if(r in e)return l[t]=r}}function o(t,e){return parseFloat(e[I(t)])||0}function s(t,e,n){void 0===n&&(n=window.getComputedStyle(t));t="border"===e?"Width":"";return{left:o("".concat(e,"Left").concat(t),n),right:o("".concat(e,"Right").concat(t),n),top:o("".concat(e,"Top").concat(t),n),bottom:o("".concat(e,"Bottom").concat(t),n)}}function W(t,e,n){t.style[I(e)]=n}function Z(t){var e=t.parentNode,n=window.getComputedStyle(t),o=window.getComputedStyle(e),r=t.getBoundingClientRect(),a=e.getBoundingClientRect();return{elem:{style:n,width:r.width,height:r.height,top:r.top,bottom:r.bottom,left:r.left,right:r.right,margin:s(t,"margin",n),border:s(t,"border",n)},parent:{style:o,width:a.width,height:a.height,top:a.top,bottom:a.bottom,left:a.left,right:a.right,padding:s(e,"padding",o),border:s(e,"border",o)}}}var q=/^http:[\w\.\/]+svg$/;var B={animate:!1,canvas:!1,cursor:"move",disablePan:!1,disableZoom:!1,disableXAxis:!1,disableYAxis:!1,duration:200,easing:"ease-in-out",exclude:[],excludeClass:"panzoom-exclude",handleStartEvent:function(t){t.preventDefault(),t.stopPropagation()},maxScale:4,minScale:.125,overflow:"hidden",panOnlyWhenZoomed:!1,pinchAndPan:!1,relative:!1,setTransform:function(t,e,n){var o=e.x,r=e.y,a=e.scale,e=e.isSVG;W(t,"transform","scale(".concat(a,") translate(").concat(o,"px, ").concat(r,"px)")),e&&i&&(a=window.getComputedStyle(t).getPropertyValue("transform"),t.setAttribute("transform",a))},startX:0,startY:0,startScale:1,step:.3,touchAction:"none"};function t(u,f){if(!u)throw new Error("Panzoom requires an element as an argument");if(1!==u.nodeType)throw new Error("Panzoom requires an element with a nodeType of 1");if(e=(t=u).ownerDocument,t=t.parentNode,!(e&&t&&9===e.nodeType&&1===t.nodeType&&e.documentElement.contains(t)))throw new Error("Panzoom should be called on elements that have been attached to the DOM");f=Y(Y({},B),f),e=u;var t,e,l=q.test(e.namespaceURI)&&"svg"!==e.nodeName.toLowerCase(),n=u.parentNode;n.style.overflow=f.overflow,n.style.userSelect="none",n.style.touchAction=f.touchAction,(f.canvas?n:u).style.cursor=f.cursor,u.style.userSelect="none",u.style.touchAction=f.touchAction,W(u,"transformOrigin","string"==typeof f.origin?f.origin:l?"0 0":"50% 50%");var r,a,i,c,s,d,m=0,h=0,v=1,p=!1;function g(t,e,n){n.silent||(n=new CustomEvent(t,{detail:e}),u.dispatchEvent(n))}function y(o,r,t){var a={x:m,y:h,scale:v,isSVG:l,originalEvent:t};return requestAnimationFrame(function(){var t,e,n;"boolean"==typeof r.animate&&(r.animate?(t=u,e=r,n=I("transform"),W(t,"transition","".concat(n," ").concat(e.duration,"ms ").concat(e.easing))):W(u,"transition","none")),r.setTransform(u,a,r),g(o,a,r),g("panzoomchange",a,r)}),a}function w(t,e,n,o){var r,a,i,c,l,s,d,o=Y(Y({},f),o),p={x:m,y:h,opts:o};return!o.force&&(o.disablePan||o.panOnlyWhenZoomed&&v===o.startScale)||(t=parseFloat(t),e=parseFloat(e),o.disableXAxis||(p.x=(o.relative?m:0)+t),o.disableYAxis||(p.y=(o.relative?h:0)+e),o.contain&&(e=((r=(e=(t=Z(u)).elem.width/v)*n)-e)/2,i=((a=(i=t.elem.height/v)*n)-i)/2,"inside"===o.contain?(c=(-t.elem.margin.left-t.parent.padding.left+e)/n,l=(t.parent.width-r-t.parent.padding.left-t.elem.margin.left-t.parent.border.left-t.parent.border.right+e)/n,p.x=Math.max(Math.min(p.x,l),c),s=(-t.elem.margin.top-t.parent.padding.top+i)/n,d=(t.parent.height-a-t.parent.padding.top-t.elem.margin.top-t.parent.border.top-t.parent.border.bottom+i)/n,p.y=Math.max(Math.min(p.y,d),s)):"outside"===o.contain&&(c=(-(r-t.parent.width)-t.parent.padding.left-t.parent.border.left-t.parent.border.right+e)/n,l=(e-t.parent.padding.left)/n,p.x=Math.max(Math.min(p.x,l),c),s=(-(a-t.parent.height)-t.parent.padding.top-t.parent.border.top-t.parent.border.bottom+i)/n,d=(i-t.parent.padding.top)/n,p.y=Math.max(Math.min(p.y,d),s))),o.roundPixels&&(p.x=Math.round(p.x),p.y=Math.round(p.y))),p}function b(t,e){var n,o,r,a,e=Y(Y({},f),e),i={scale:v,opts:e};return!e.force&&e.disableZoom||(n=f.minScale,o=f.maxScale,e.contain&&(a=(e=Z(u)).elem.width/v,r=e.elem.height/v,1<a&&1<r&&(a=(e.parent.width-e.parent.border.left-e.parent.border.right)/a,e=(e.parent.height-e.parent.border.top-e.parent.border.bottom)/r,"inside"===f.contain?o=Math.min(o,a,e):"outside"===f.contain&&(n=Math.max(n,a,e)))),i.scale=Math.min(Math.max(t,n),o)),i}function x(t,e,n,o){t=w(t,e,v,n);return m!==t.x||h!==t.y?(m=t.x,h=t.y,y("panzoompan",t.opts,o)):{x:m,y:h,scale:v,isSVG:l,originalEvent:o}}function E(t,e,n){var o,r,e=b(t,e),a=e.opts;if(a.force||!a.disableZoom)return t=e.scale,e=m,o=h,a.focal&&(e=((r=a.focal).x/t-r.x/v+m*t)/t,o=(r.y/t-r.y/v+h*t)/t),r=w(e,o,t,{relative:!1,force:!0}),m=r.x,h=r.y,v=t,y("panzoomzoom",a,n)}function o(t,e){e=Y(Y(Y({},f),{animate:!0}),e);return E(v*Math.exp((t?1:-1)*e.step),e)}function S(t,e,n,o){var r=Z(u),a=r.parent.width-r.parent.padding.left-r.parent.padding.right-r.parent.border.left-r.parent.border.right,i=r.parent.height-r.parent.padding.top-r.parent.padding.bottom-r.parent.border.top-r.parent.border.bottom,c=e.clientX-r.parent.left-r.parent.padding.left-r.parent.border.left-r.elem.margin.left,e=e.clientY-r.parent.top-r.parent.padding.top-r.parent.border.top-r.elem.margin.top,r=(l||(c-=r.elem.width/v/2,e-=r.elem.height/v/2),{x:c/a*(a*t),y:e/i*(i*t)});return E(t,Y(Y({},n),{animate:!1,focal:r}),o)}E(f.startScale,{animate:!1,force:!0}),setTimeout(function(){x(f.startX,f.startY,{animate:!1,force:!0})});var M=[];function A(t){!function(t,e){for(var n,o,r=t;null!=r;r=r.parentNode)if(n=r,o=e.excludeClass,1===n.nodeType&&-1<" ".concat((n.getAttribute("class")||"").trim()," ").indexOf(" ".concat(o," "))||-1<e.exclude.indexOf(r))return 1}(t.target,f)&&(T(M,t),p=!0,f.handleStartEvent(t),g("panzoomstart",{x:r=m,y:a=h,scale:v,isSVG:l,originalEvent:t},f),t=N(M),i=t.clientX,c=t.clientY,s=v,d=L(M))}function P(t){var e,n,o;p&&void 0!==r&&void 0!==a&&void 0!==i&&void 0!==c&&(T(M,t),e=N(M),n=1<M.length,o=v,n&&(0===d&&(d=L(M)),S(o=b((L(M)-d)*f.step/80+s).scale,e,{animate:!1},t)),n&&!f.pinchAndPan||x(r+(e.clientX-i)/o,a+(e.clientY-c)/o,{animate:!1},t))}function O(t){1===M.length&&g("panzoomend",{x:m,y:h,scale:v,isSVG:l,originalEvent:t},f);var e=M;if(t.touches)for(;e.length;)e.pop();else{t=C(e,t);-1<t&&e.splice(t,1)}p&&(p=!1,r=a=i=c=void 0)}var z=!1;function X(){z||(z=!0,D("down",f.canvas?n:u,A),D("move",document,P,{passive:!0}),D("up",document,O,{passive:!0}))}return f.noBind||X(),{bind:X,destroy:function(){z=!1,G("down",f.canvas?n:u,A),G("move",document,P),G("up",document,O)},eventNames:V,getPan:function(){return{x:m,y:h}},getScale:function(){return v},getOptions:function(){var t,e=f,n={};for(t in e)e.hasOwnProperty(t)&&(n[t]=e[t]);return n},handleDown:A,handleMove:P,handleUp:O,pan:x,reset:function(t){var t=Y(Y(Y({},f),{animate:!0,force:!0}),t),e=(v=b(t.startScale,t).scale,w(t.startX,t.startY,v,t));return m=e.x,h=e.y,y("panzoomreset",t)},resetStyle:function(){n.style.overflow="",n.style.userSelect="",n.style.touchAction="",n.style.cursor="",u.style.cursor="",u.style.userSelect="",u.style.touchAction="",W(u,"transformOrigin","")},setOptions:function(t){for(var e in t=void 0===t?{}:t)t.hasOwnProperty(e)&&(f[e]=t[e]);(t.hasOwnProperty("cursor")||t.hasOwnProperty("canvas"))&&(n.style.cursor=u.style.cursor="",(f.canvas?n:u).style.cursor=f.cursor),t.hasOwnProperty("overflow")&&(n.style.overflow=t.overflow),t.hasOwnProperty("touchAction")&&(n.style.touchAction=t.touchAction,u.style.touchAction=t.touchAction)},setStyle:function(t,e){return W(u,t,e)},zoom:E,zoomIn:function(t){return o(!0,t)},zoomOut:function(t){return o(!1,t)},zoomToPoint:S,zoomWithWheel:function(t,e){t.preventDefault();var e=Y(Y(Y({},f),e),{animate:!1}),n=0===t.deltaY&&t.deltaX?t.deltaX:t.deltaY;return S(b(v*Math.exp((n<0?1:-1)*e.step/3),e).scale,t,e,t)}}}return t.defaultOptions=B,t});
"""

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_KICAD_CLI_CHECKED = False
_KICAD_CLI_AVAILABLE = False


def _warn(warnings_list: List[str], msg: str) -> None:
    print(f"WARNING: {msg}", file=sys.stderr)
    warnings_list.append(msg)


def _check_kicad_cli(warnings_list: List[str]) -> bool:
    global _KICAD_CLI_CHECKED, _KICAD_CLI_AVAILABLE
    if _KICAD_CLI_CHECKED:
        return _KICAD_CLI_AVAILABLE
    _KICAD_CLI_CHECKED = True
    result = subprocess.run(["which", "kicad-cli"], capture_output=True)
    _KICAD_CLI_AVAILABLE = result.returncode == 0
    if not _KICAD_CLI_AVAILABLE:
        _warn(warnings_list, "kicad-cli not found on PATH — SVG export skipped for all sheets")
    return _KICAD_CLI_AVAILABLE


# ---------------------------------------------------------------------------
# Step 1 — Discover schematics
# ---------------------------------------------------------------------------

def _collect_sheets(root: Path, feature: str) -> Dict[str, Path]:
    """Return {sheet_filename: absolute_path} for a given root dir."""
    sheets: Dict[str, Path] = {}

    # Primary location: features/<feature>/schematics/*.kicad_sch
    sch_dir = root / "features" / feature / "schematics"
    if sch_dir.is_dir():
        for f in sorted(sch_dir.glob("*.kicad_sch")):
            sheets[f.name] = f

    # Fallback: features/<feature>/<feature>.kicad_sch
    fallback = root / "features" / feature / f"{feature}.kicad_sch"
    if fallback.is_file() and fallback.name not in sheets:
        sheets[fallback.name] = fallback

    return sheets


def find_sheets(
    base_dir: Path, head_dir: Path, feature: str
) -> Dict[str, Tuple[Optional[Path], Optional[Path]]]:
    """Return {sheet_name: (base_path_or_None, head_path_or_None)}."""
    base_sheets = _collect_sheets(base_dir, feature)
    head_sheets = _collect_sheets(head_dir, feature)
    all_names = sorted(set(base_sheets) | set(head_sheets))
    return {
        name: (base_sheets.get(name), head_sheets.get(name))
        for name in all_names
    }


# ---------------------------------------------------------------------------
# Step 2 — Export SVG
# ---------------------------------------------------------------------------

def export_svg(
    sch_path: Path, svg_out_dir: Path, warnings_list: List[str]
) -> Optional[Path]:
    """Run kicad-cli and return path of exported SVG, or None on failure."""
    svg_out_dir.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["kicad-cli", "sch", "export", "svg",
         "--output", str(svg_out_dir),
         str(sch_path)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        _warn(
            warnings_list,
            f"kicad-cli failed for {sch_path.name}: "
            f"{(result.stderr or result.stdout or '').strip()[:300]}",
        )
        return None

    # kicad-cli typically names the output <stem>.svg in the output directory
    expected = svg_out_dir / (sch_path.stem + ".svg")
    if expected.is_file():
        return expected

    # Fallback: pick any SVG that appeared in the output dir
    svgs = sorted(svg_out_dir.glob("*.svg"))
    if svgs:
        return svgs[0]

    _warn(warnings_list, f"kicad-cli ran but no SVG found for {sch_path.name}")
    return None


# ---------------------------------------------------------------------------
# Step 3 — Rasterise SVG → PNG
# ---------------------------------------------------------------------------

def rasterize_svg(
    svg_path: Path, png_path: Path, warnings_list: List[str]
) -> bool:
    """Convert SVG to PNG. Returns True on success."""
    png_path.parent.mkdir(parents=True, exist_ok=True)

    # Try cairosvg first
    if CAIROSVG_AVAILABLE:
        try:
            cairosvg.svg2png(  # type: ignore[misc]
                url=str(svg_path), write_to=str(png_path), scale=2.0
            )
            if png_path.is_file():
                return True
        except Exception as exc:
            _warn(warnings_list, f"cairosvg failed for {svg_path.name}: {exc}")

    # Try inkscape fallback
    try:
        result = subprocess.run(
            [
                "inkscape",
                "--export-type=png",
                f"--export-filename={png_path}",
                "--export-dpi=150",
                str(svg_path),
            ],
            capture_output=True,
        )
        if result.returncode == 0 and png_path.is_file():
            return True
    except FileNotFoundError:
        pass  # inkscape not installed

    _warn(
        warnings_list,
        f"Neither cairosvg nor inkscape could rasterize {svg_path.name} "
        f"— sheet marked as unrenderable",
    )
    return False


# ---------------------------------------------------------------------------
# Step 4 — Compute pixel diff
# ---------------------------------------------------------------------------

_TOLERANCE = 10
_WHITE_THRESHOLD = 255 - _TOLERANCE  # 245


def _pad_to_same_size(
    img1: "Image.Image", img2: "Image.Image"
) -> Tuple["Image.Image", "Image.Image"]:
    w = max(img1.width, img2.width)
    h = max(img1.height, img2.height)

    def _pad(img: "Image.Image") -> "Image.Image":
        if img.size == (w, h):
            return img
        canvas = Image.new("RGB", (w, h), (255, 255, 255))
        canvas.paste(img, (0, 0))
        return canvas

    return _pad(img1), _pad(img2)


def _compute_diff_numpy(
    img_base: "Image.Image",
    img_head: "Image.Image",
    diff_path: Path,
    warnings_list: List[str],
) -> bool:
    """Pixel diff using numpy arrays (fast)."""
    try:
        arr_b = np.array(img_base, dtype=np.int16)
        arr_h = np.array(img_head, dtype=np.int16)

        diff = np.abs(arr_b - arr_h)
        changed = diff.max(axis=2) > _TOLERANCE

        base_white = arr_b.min(axis=2) >= _WHITE_THRESHOLD
        head_white = arr_h.min(axis=2) >= _WHITE_THRESHOLD

        removed = changed & ~base_white & head_white   # magenta
        added   = changed & base_white & ~head_white   # cyan
        altered = changed & ~base_white & ~head_white  # amber

        out = np.full((arr_b.shape[0], arr_b.shape[1], 3), 220, dtype=np.uint8)
        out[removed] = [255,   0, 255]
        out[added]   = [  0, 220, 220]
        out[altered] = [255, 180,   0]

        Image.fromarray(out, "RGB").save(diff_path)
        return True
    except Exception as exc:
        _warn(warnings_list, f"numpy diff failed: {exc}")
        return False


def _compute_diff_pillow(
    img_base: "Image.Image",
    img_head: "Image.Image",
    diff_path: Path,
    warnings_list: List[str],
) -> bool:
    """Pixel diff using pure Pillow (slower, no numpy required)."""
    try:
        w, h = img_base.width, img_base.height
        out = Image.new("RGB", (w, h), (220, 220, 220))

        base_pixels = img_base.load()
        head_pixels = img_head.load()
        out_pixels  = out.load()

        for y in range(h):
            for x in range(w):
                rb, gb, bb = base_pixels[x, y][:3]  # type: ignore[index]
                rh, gh, bh = head_pixels[x, y][:3]  # type: ignore[index]

                diff_r = abs(rb - rh)
                diff_g = abs(gb - gh)
                diff_b = abs(bb - bh)

                if max(diff_r, diff_g, diff_b) <= _TOLERANCE:
                    # identical
                    out_pixels[x, y] = (220, 220, 220)
                    continue

                base_is_white = rb >= _WHITE_THRESHOLD and gb >= _WHITE_THRESHOLD and bb >= _WHITE_THRESHOLD
                head_is_white = rh >= _WHITE_THRESHOLD and gh >= _WHITE_THRESHOLD and bh >= _WHITE_THRESHOLD

                if not base_is_white and head_is_white:
                    out_pixels[x, y] = (255, 0, 255)    # removed — magenta
                elif base_is_white and not head_is_white:
                    out_pixels[x, y] = (0, 220, 220)    # added — cyan
                else:
                    out_pixels[x, y] = (255, 180, 0)    # changed — amber

        out.save(diff_path)
        return True
    except Exception as exc:
        _warn(warnings_list, f"Pillow diff failed: {exc}")
        return False


def compute_diff(
    base_png: Path, head_png: Path, diff_path: Path, warnings_list: List[str]
) -> bool:
    """Generate diff image between two PNG files. Returns True on success."""
    if not PILLOW_AVAILABLE:
        _warn(warnings_list, "Pillow not available — cannot compute pixel diff")
        return False

    try:
        img_base = Image.open(base_png).convert("RGB")
        img_head = Image.open(head_png).convert("RGB")
        img_base, img_head = _pad_to_same_size(img_base, img_head)
    except Exception as exc:
        _warn(warnings_list, f"Failed to open images for diff: {exc}")
        return False

    if NUMPY_AVAILABLE:
        return _compute_diff_numpy(img_base, img_head, diff_path, warnings_list)
    return _compute_diff_pillow(img_base, img_head, diff_path, warnings_list)


# ---------------------------------------------------------------------------
# Step 5 — Generate outputs
# ---------------------------------------------------------------------------

def _img_tag(path: Optional[Path], sheet_slug: str = "", side: str = "") -> str:
    """Return an <img> HTML tag with base64-embedded PNG, or em dash.

    When sheet_slug and side are provided, wraps the image in a panzoom
    container with a reset button.
    """
    if path is None or not path.is_file():
        return "&mdash;"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    uri = f"data:image/png;base64,{data}"
    img = f'<img src="{uri}" style="max-width:400px;height:auto;" alt="">'
    if sheet_slug and side:
        pz_id = f"pz-{sheet_slug}-{side}"
        return (
            f'<div class="pz-wrap">'
            f'<div class="pz-elem" id="{pz_id}">{img}</div>'
            f'<button class="pz-reset" onclick="resetPz(\'{pz_id}\')">&#x27F3; Reset</button>'
            f'</div>'
        )
    return img


def generate_html(
    feature: str,
    sheets: Dict[str, Tuple[Optional[Path], Optional[Path]]],
    results: Dict[str, dict],
    base_sha: str,
    head_sha: str,
    ts: str,
) -> str:
    rows_html_parts = []
    for name in sheets:
        r = results.get(name, {})
        status = r.get("status", "unrenderable")
        sheet_slug = name.replace(".", "_")

        if status == "unrenderable":
            cell = (
                '<td colspan="3" class="warn">'
                "&#9888;&#xFE0F; Could not render this sheet &mdash; check workflow logs"
                "</td>"
            )
            rows_html_parts.append(
                f"<tr><td><code>{name}</code></td>{cell}</tr>"
            )
        elif status == "new":
            head_img = _img_tag(r.get("head_png"), sheet_slug, "new")
            rows_html_parts.append(
                f"<tr><td><code>{name}</code></td>"
                f"<td>&mdash;</td>"
                f"<td><span class='badge badge-new'>&#x1F195; New sheet</span></td>"
                f"<td>{head_img}</td></tr>"
            )
        elif status == "deleted":
            base_img = _img_tag(r.get("base_png"), sheet_slug, "base")
            rows_html_parts.append(
                f"<tr><td><code>{name}</code></td>"
                f"<td>{base_img}</td>"
                f"<td><span class='badge badge-deleted'>&#x1F5D1;&#xFE0F; Deleted</span></td>"
                f"<td>&mdash;</td></tr>"
            )
        else:  # compared
            base_img = _img_tag(r.get("base_png"), sheet_slug, "base")
            diff_img = _img_tag(r.get("diff_png"), sheet_slug, "diff")
            head_img = _img_tag(r.get("head_png"), sheet_slug, "new")
            rows_html_parts.append(
                f"<tr><td><code>{name}</code></td>"
                f"<td>{base_img}</td>"
                f"<td>{diff_img}</td>"
                f"<td>{head_img}</td></tr>"
            )

    rows_html = "\n".join(rows_html_parts)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Visual Diff &mdash; {feature}</title>
<style>
  body {{ font-family: sans-serif; margin: 1em 2em; color: #222; }}
  h1   {{ font-size: 1.4em; }}
  .legend {{ display: flex; flex-wrap: wrap; gap: 1.5em; margin: 1em 0 2em; align-items: center; }}
  .swatch {{ display: inline-block; width: 20px; height: 20px;
             border: 1px solid #999; vertical-align: middle; margin-right: 4px; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th, td {{ border: 1px solid #ccc; padding: 0.5em; vertical-align: top; }}
  th {{ background: #f5f5f5; text-align: left; }}
  .warn {{ background: #fff8dc; color: #8a6d00; }}
  .badge {{ padding: 0.2em 0.6em; border-radius: 4px; font-size: 0.9em;
            display: inline-block; }}
  .badge-new {{ background: #00DCDC; color: #000; }}
  .badge-deleted {{ background: #FF00FF; color: #fff; }}
  footer {{ margin-top: 2em; font-size: 0.85em; color: #666;
            border-top: 1px solid #eee; padding-top: 0.5em; }}
  .pz-wrap {{ display: inline-block; border: 1px solid #ddd; overflow: hidden;
              position: relative; max-width: 420px; }}
  .pz-elem {{ cursor: grab; }}
  .pz-elem:active {{ cursor: grabbing; }}
  .pz-reset {{ position: absolute; top: 4px; right: 4px; font-size: 0.75em;
               padding: 2px 6px; background: rgba(255,255,255,0.85);
               border: 1px solid #aaa; border-radius: 3px; cursor: pointer; }}
</style>
</head>
<body>
<h1>Visual Diff &mdash; <code>{feature}</code></h1>

<div class="legend">
  <span><span class="swatch" style="background:#00DCDC"></span> Added (cyan)</span>
  <span><span class="swatch" style="background:#FF00FF"></span> Removed (magenta)</span>
  <span><span class="swatch" style="background:#FFB400"></span> Changed (amber)</span>
  <span><span class="swatch" style="background:#DCDCDC"></span> Unchanged (grey)</span>
</div>

<table>
  <thead>
    <tr><th>Sheet</th><th>Old (base)</th><th>Diff</th><th>New (head)</th></tr>
  </thead>
  <tbody>
{rows_html}
  </tbody>
</table>

<footer>
  Feature: <code>{feature}</code> &nbsp;|&nbsp;
  BASE_SHA: <code>{base_sha}</code> &nbsp;|&nbsp;
  HEAD_SHA: <code>{head_sha}</code> &nbsp;|&nbsp;
  Generated: {ts}
</footer>
<script>
// panzoom v4.5.1 — MIT licence — https://github.com/timmywil/panzoom
{_PANZOOM_JS}
const pzInstances = {{}};
document.querySelectorAll('.pz-elem').forEach(el => {{
  pzInstances[el.id] = Panzoom(el, {{ maxScale: 8, minScale: 0.5 }});
  el.parentElement.addEventListener('wheel', pzInstances[el.id].zoomWithWheel);
}});
function resetPz(id) {{
  if (pzInstances[id]) pzInstances[id].reset();
}}
</script>
</body>
</html>
"""


def generate_comment_md(
    feature: str,
    sheets: Dict[str, Tuple[Optional[Path], Optional[Path]]],
    results: Dict[str, dict],
    warnings_list: List[str],
) -> str:
    lines: List[str] = [
        f"### \U0001f5bc\ufe0f Visual Diff \u2014 `{feature}`",
        "",
        "| Sheet | Result |",
        "|---|---|",
    ]
    for name in sheets:
        r = results.get(name, {})
        status = r.get("status", "unrenderable")
        if status == "new":
            result_str = "\U0001f195 New sheet"
        elif status == "deleted":
            result_str = "\U0001f5d1\ufe0f Deleted"
        elif status == "unrenderable":
            result_str = "\u26a0\ufe0f Could not render"
        else:
            result_str = "\u2705 Diff generated"
        lines.append(f"| `{name}` | {result_str} |")

    lines.append("")
    lines.append(
        "\U0001f4e5 Full HTML diff report available in workflow artifacts (90-day retention)."
    )

    if warnings_list:
        lines.append("")
        lines.append(f"<details><summary>\u26a0\ufe0f Warnings ({len(warnings_list)})</summary>")
        lines.append("")
        for w in warnings_list:
            lines.append(f"- {w}")
        lines.append("")
        lines.append("</details>")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Per-sheet processing helpers
# ---------------------------------------------------------------------------

def _process_side(
    sch_path: Optional[Path],
    side: str,
    svg_dir: Path,
    png_dir: Path,
    kicad_available: bool,
    warnings_list: List[str],
) -> Optional[Path]:
    """Export SVG and rasterise to PNG for one side (base or head)."""
    if sch_path is None:
        return None
    if not kicad_available:
        return None

    svg_out = svg_dir / side
    svg_path = export_svg(sch_path, svg_out, warnings_list)
    if svg_path is None:
        return None

    png_path = png_dir / side / (sch_path.stem + ".png")
    if rasterize_svg(svg_path, png_path, warnings_list):
        return png_path
    return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a visual diff of KiCad schematic sheets."
    )
    parser.add_argument("--base-dir",   required=True, type=Path,
                        help="Directory containing the base (old) files")
    parser.add_argument("--head-dir",   required=True, type=Path,
                        help="Directory containing the head (new) files")
    parser.add_argument("--feature",    required=True,
                        help="Feature name (e.g. buck-converter-5v)")
    parser.add_argument("--output-dir", required=True, type=Path,
                        help="Directory where outputs will be written")
    args = parser.parse_args()

    base_dir: Path  = args.base_dir
    head_dir: Path  = args.head_dir
    feature: str    = args.feature
    out_dir: Path   = args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    warnings_list: List[str] = []
    base_sha = os.environ.get("BASE_SHA", "unknown")
    head_sha = os.environ.get("HEAD_SHA", "unknown")
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # ---- Step 1: Discover schematics ----------------------------------------
    sheets = find_sheets(base_dir, head_dir, feature)
    if not sheets:
        _warn(
            warnings_list,
            f"No .kicad_sch files found for feature '{feature}' "
            f"in either base-dir or head-dir",
        )

    # ---- Step 2: Check kicad-cli availability --------------------------------
    kicad_available = _check_kicad_cli(warnings_list)

    # Working subdirectories
    svg_dir  = out_dir / "svgs"
    png_dir  = out_dir / "pngs"
    diff_dir = out_dir / "diffs"
    for d in (svg_dir, png_dir, diff_dir):
        d.mkdir(parents=True, exist_ok=True)

    results: Dict[str, dict] = {}
    sheets_compared: List[str] = []
    sheets_new:      List[str] = []
    sheets_deleted:  List[str] = []

    for name, (base_sch, head_sch) in sheets.items():
        r: dict = {}

        # Classify sheet
        if base_sch is None:
            status = "new"
            sheets_new.append(name)
        elif head_sch is None:
            status = "deleted"
            sheets_deleted.append(name)
        else:
            status = "compared"
            sheets_compared.append(name)

        r["status"] = status

        # ---- Steps 2 + 3: Export and rasterise --------------------------------
        base_png = _process_side(
            base_sch, "base", svg_dir, png_dir, kicad_available, warnings_list
        )
        head_png = _process_side(
            head_sch, "head", svg_dir, png_dir, kicad_available, warnings_list
        )

        if base_png:
            r["base_png"] = base_png
        if head_png:
            r["head_png"] = head_png

        # ---- Step 4: Compute pixel diff (compared sheets only) ----------------
        if status == "compared":
            if base_png is None or head_png is None:
                r["status"] = "unrenderable"
                _warn(
                    warnings_list,
                    f"Cannot diff {name}: "
                    f"{'base' if base_png is None else 'head'} side could not be rendered",
                )
            else:
                diff_path = diff_dir / (Path(name).stem + "-diff.png")
                if compute_diff(base_png, head_png, diff_path, warnings_list):
                    r["diff_png"] = diff_path
                else:
                    r["status"] = "unrenderable"

        elif status in ("new", "deleted"):
            # Mark unrenderable only if kicad-cli is available but rendering failed
            side_png = head_png if status == "new" else base_png
            if side_png is None and kicad_available:
                r["status"] = "unrenderable"

        results[name] = r

    # ---- Step 5: Generate outputs -------------------------------------------

    # diff-report.html
    html_content = generate_html(
        feature, sheets, results, base_sha, head_sha, ts
    )
    (out_dir / "diff-report.html").write_text(html_content, encoding="utf-8")

    # metadata.json
    metadata = {
        "feature":          feature,
        "base_sha":         base_sha,
        "head_sha":         head_sha,
        "sheets_compared":  sheets_compared,
        "sheets_new":       sheets_new,
        "sheets_deleted":   sheets_deleted,
        "warnings":         warnings_list,
    }
    (out_dir / "metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # comment.md
    comment_md = generate_comment_md(feature, sheets, results, warnings_list)
    (out_dir / "comment.md").write_text(comment_md, encoding="utf-8")

    print(f"kicad-visual-diff complete. Outputs in {out_dir}")
    print(f"  Sheets compared: {len(sheets_compared)}, "
          f"new: {len(sheets_new)}, deleted: {len(sheets_deleted)}")
    if warnings_list:
        print(f"  {len(warnings_list)} warning(s):")
        for w in warnings_list:
            print(f"    - {w}")

    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        print(f"FATAL: {exc}", file=sys.stderr)
        sys.exit(0)  # always exit 0
