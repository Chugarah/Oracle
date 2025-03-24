# Changelog

## [1.1.0] - 2023-09-10

### Added
- Progress options for controlling download progress display
- Support for customizing progress options at global, source, and item levels
- Improved error handling for yt-dlp downloads
- Enhanced documentation for progress options in README.md

### Changed
- Replaced custom progress hook with yt-dlp's native progress reporting
- Simplified download logic for better stability
- Improved error diagnostics and recovery
- Enhanced configuration structure for better organization

### Fixed
- Fixed type conversion errors in progress display
- Resolved issues with custom progress templates
- Improved handling of yt-dlp configuration options
- Enhanced stability for various download scenarios

## [1.0.0] - 2023-07-15

### Added
- Initial release
- Support for YouTube and TikTok downloads
- Multi-threaded downloading
- FFMPEG post-processing
- Custom output templates
- Configuration via YAML and JSON files

## [2.0.0] - 2024-03-22

### Added
- New YAML configuration system for application settings
- JSON-based media library for organizing download sources
- Support for multiple source types (YouTube, TikTok, etc.)
- Source-specific configuration options
- Configuration test script for verifying setup
- Comprehensive documentation for the new configuration system

### Changed
- Completely refactored settings module to use YAML
- Updated downloader module to use YT-DLP's Python API more effectively
- Improved progress tracking with enhanced progress hooks
- Refactored main script to use the new configuration structure
- Enhanced README with detailed configuration information

### Removed
- Legacy worker thread implementation
- Manual URL type detection (now handled by YT-DLP)
- Redundant file processing code

## [1.0.0] - Prior to 2024-03-22

Initial version with basic downloader functionality. 