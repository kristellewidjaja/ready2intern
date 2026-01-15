# LLM Service Configuration Guide

## Overview

The LLM service can be configured via environment variables in your `.env` file. This allows you to customize the Claude model, retry behavior, and other settings without changing code.

## Configuration Options

### Required Configuration

```bash
# Your Anthropic API key (required)
ANTHROPIC_API_KEY=sk-ant-api03-...your-key-here...
```

### Optional LLM Configuration

```bash
# Claude model to use (default: claude-3-5-sonnet-20241022)
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# Maximum number of retry attempts on API failures (default: 3)
LLM_MAX_RETRIES=3

# Base delay in seconds for exponential backoff (default: 1)
# Actual delays will be: 1s, 2s, 4s for 3 retries
LLM_RETRY_DELAY=1
```

## Available Claude Models

### Recommended Models

| Model | ID | Best For | Speed | Cost | Quality |
|-------|-----|----------|-------|------|---------|
| **Claude 3.5 Sonnet** | `claude-3-5-sonnet-20241022` | General use (default) | Fast | Medium | High |
| **Claude 3.5 Haiku** | `claude-3-5-haiku-20241022` | Simple resumes, high volume | Very Fast | Low | Good |
| **Claude 3 Opus** | `claude-3-opus-20240229` | Complex resumes, max accuracy | Slow | High | Highest |

### Model Selection Guide

**Use Claude 3.5 Sonnet (default) when:**
- Processing typical internship resumes
- You want the best balance of speed, cost, and quality
- This is the recommended model for most use cases

**Use Claude 3.5 Haiku when:**
- Processing simple, straightforward resumes
- You need faster response times (5-10 seconds vs 10-20 seconds)
- You're processing high volumes and want to reduce costs
- Cost is ~5x cheaper than Sonnet

**Use Claude 3 Opus when:**
- Processing complex or lengthy resumes (3+ pages)
- You need maximum accuracy for executive or senior roles
- Quality is more important than speed or cost
- Cost is ~5x more expensive than Sonnet

## Retry Configuration

### Max Retries

Controls how many times the service will retry on transient failures:

```bash
LLM_MAX_RETRIES=3  # Default: try up to 3 times
```

**When to adjust:**
- **Increase to 5-10**: If you experience frequent rate limits or timeouts
- **Decrease to 1-2**: If you want faster failure feedback
- **Set to 0**: To disable retries (not recommended)

### Retry Delay

Controls the base delay for exponential backoff:

```bash
LLM_RETRY_DELAY=1  # Default: 1 second base delay
```

**Exponential backoff calculation:**
- Retry 1: `base_delay * 2^0` = 1 second
- Retry 2: `base_delay * 2^1` = 2 seconds
- Retry 3: `base_delay * 2^2` = 4 seconds

**When to adjust:**
- **Increase to 2-3**: If you're hitting rate limits frequently
- **Decrease to 0.5**: For faster retries (may hit rate limits more)

## Example Configurations

### Development (Fast & Cheap)

```bash
ANTHROPIC_API_KEY=your_key_here
ANTHROPIC_MODEL=claude-3-5-haiku-20241022
LLM_MAX_RETRIES=2
LLM_RETRY_DELAY=1
```

**Use case:** Testing, development, simple resumes

### Production (Balanced)

```bash
ANTHROPIC_API_KEY=your_key_here
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
LLM_MAX_RETRIES=3
LLM_RETRY_DELAY=1
```

**Use case:** Most production workloads (this is the default)

### High Quality (Accurate)

```bash
ANTHROPIC_API_KEY=your_key_here
ANTHROPIC_MODEL=claude-3-opus-20240229
LLM_MAX_RETRIES=5
LLM_RETRY_DELAY=2
```

**Use case:** Complex resumes, maximum accuracy needed

### High Volume (Cost Optimized)

```bash
ANTHROPIC_API_KEY=your_key_here
ANTHROPIC_MODEL=claude-3-5-haiku-20241022
LLM_MAX_RETRIES=2
LLM_RETRY_DELAY=1
```

**Use case:** Processing hundreds/thousands of resumes

## Cost Comparison

Based on a typical resume (~2,250 tokens total):

| Model | Cost per Resume | Cost per 100 Resumes | Cost per 1,000 Resumes |
|-------|----------------|---------------------|----------------------|
| Claude 3.5 Haiku | ~$0.004 | ~$0.40 | ~$4.00 |
| Claude 3.5 Sonnet | ~$0.019 | ~$1.90 | ~$19.00 |
| Claude 3 Opus | ~$0.095 | ~$9.50 | ~$95.00 |

## Testing Configuration

To test different configurations:

```bash
# Edit your .env file
nano backend/.env

# Restart the backend server
# The new configuration will be loaded on startup

# Run a test analysis
cd backend
./quick_test.sh
```

## Troubleshooting

### "Model not found" error

**Problem:** Invalid model ID in `ANTHROPIC_MODEL`

**Solution:** Use one of the valid model IDs listed above

### Rate limit errors even with retries

**Problem:** Too many requests in short time

**Solution:** 
- Increase `LLM_RETRY_DELAY` to 2 or 3
- Increase `LLM_MAX_RETRIES` to 5 or more
- Add delays between batch processing

### Slow response times

**Problem:** Model is too slow for your needs

**Solution:**
- Switch to `claude-3-5-haiku-20241022` for faster responses
- Reduce `LLM_MAX_RETRIES` to fail faster

### High costs

**Problem:** Processing many resumes is expensive

**Solution:**
- Switch to `claude-3-5-haiku-20241022` (5x cheaper)
- Reduce `LLM_MAX_RETRIES` to avoid multiple API calls on failures

## Environment Variable Precedence

1. **Environment variables** (highest priority)
2. **Default values** in code (fallback)

This means:
- If `ANTHROPIC_MODEL` is set, it will be used
- If not set, defaults to `claude-3-5-sonnet-20241022`
- Same logic applies to all optional configuration

## Validation

The service validates configuration on startup:

```python
# Required
ANTHROPIC_API_KEY must be set (raises ValueError if missing)

# Optional (uses defaults if not set)
ANTHROPIC_MODEL defaults to "claude-3-5-sonnet-20241022"
LLM_MAX_RETRIES defaults to 3
LLM_RETRY_DELAY defaults to 1
```

## Logging

The service logs its configuration on startup:

```
INFO:app.services.llm_service:LLMService initialized with model: claude-3-5-sonnet-20241022
```

Check your backend logs to verify the configuration is loaded correctly.

## Best Practices

1. **Start with defaults** - The default configuration works well for most cases
2. **Test changes** - Always test after changing configuration
3. **Monitor costs** - Track API usage and costs in Anthropic console
4. **Use Haiku for dev** - Save money during development/testing
5. **Use Sonnet for prod** - Best balance for production workloads
6. **Reserve Opus for special cases** - Only when you need maximum quality

## Related Documentation

- [MANUAL_TEST.md](MANUAL_TEST.md) - Manual testing guide
- [AGENTS.md](../AGENTS.md) - Implementation details
- [Anthropic API Documentation](https://docs.anthropic.com/) - Official API docs
