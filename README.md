# AI Power Grid Image Model Reference

Model reference for [AI Power Grid](https://github.com/AIPowerGrid) and [ComfyUI Bridge](https://github.com/AIPowerGrid/comfy-bridge).

This repository contains a curated collection of model definitions that bridge ComfyUI with AI Power Grid's distributed computing network. Unlike traditional model references, this system supports multiple model names per reference to accommodate the various naming conventions used in ComfyUI workflows.

## Purpose

The AI Power Grid Image Model Reference serves as a translation layer between:
- **ComfyUI** - Local AI image generation workflows
- **AI Power Grid** - Distributed computing network for AI tasks
- **ComfyUI Bridge** - Connector that enables seamless integration

## Key Features

### Multiple Model Names Support
Each model reference can include multiple names that users might encounter in ComfyUI:
- Official model names (e.g., "SDXL 1.0")
- Common aliases (e.g., "sdxl", "sdxl_base")
- File-based names (e.g., "sdxl_1_0.safetensors")
- Community variations (e.g., "stable-diffusion-xl-base-1.0")

### Baseline Model Mapping
Models are mapped to baseline types for consistent processing:
- `stable_diffusion_xl` - SDXL models
- `stable diffusion 1` - SD1.5 models  
- `stable diffusion 2` - SD2.x models
- `flux_1` - Flux models
- `stable_cascade` - Cascade models

## Model Reference Structure

```json
{
  "Model Name": {
    "name": "Official Model Name",
    "baseline": "stable_diffusion_xl",
    "type": "ckpt",
    "description": "Model description",
    "version": "1.0",
    "download_url": "https://example.com/model.safetensors",
    "sha256": "model_hash_here"
  }
}
```

## Integration with ComfyUI Bridge

The [ComfyUI Bridge](https://github.com/AIPowerGrid/comfy-bridge) uses this reference to:
1. **Translate model names** from ComfyUI workflows to AI Power Grid compatible formats
2. **Validate model availability** across the distributed network
3. **Ensure consistency** between local and distributed processing

## Adding Models

When adding new models to the reference:

To add new models, please submit a request including:
1.  **Multiple name variations** used in ComfyUI.
2.  The **correct baseline** for processing.
3.  **Accurate metadata** (version, description, etc.).
4.  Confirmation of **ComfyUI Bridge compatibility**.


## Related Projects

- [AI Power Grid](https://github.com/AIPowerGrid) - Distributed AI computing network
- [ComfyUI Bridge](https://github.com/AIPowerGrid/comfy-bridge) - ComfyUI integration
- [Grid Styles](https://github.com/AIPowerGrid/grid-styles) - Style definitions for AI Power Grid
