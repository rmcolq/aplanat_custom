# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.4.0]
### Added
- `facet_grid` function can now create a single-facet plot.
- Helper function to export JSX file for import into MDX markdown.
- Table class that uses simple table instead of bokeh.
- Add logging helper functions to util.
- Decorator which plots a null graph if plotting function fails.

## [v0.3.12]
### Added
- Ability to pass workflow revision and commit.

## [v0.3.11]
### Changed
- Abbreviated legend names for visibility in overall BP summary.
- Updated documentation in coverage panel to match fixes in mapula.

## [v0.3.10]
### Added
- Standard workflow report layout for ONT workflows.

## [v0.3.9]
### Fixed
- Fixed a bug in clone validation report parsing maf files.

## [v0.3.8]
### Added
- Added a minimal reporting component for wf-clone-validation.

## [v0.3.7]
### Changed
- Updated version of nextflow javascript component.

## [v0.3.6]
### Fixed
- Correct conda package versioning.

## [v0.3.5]
### Fixed
- Added missing module.

## [v0.3.4]
### Added
- Read stats module report component based on fastcat.

## [v0.3.3]
### Changed
- Refactored Nextclade and mapula report components.
### Added
- Deployment to epi2melabs conda channel.

## [v0.3.2]
### Added
- Report component for wf-alignment specific mapula output.

## [v0.3.1]
### Added
- Additional colour definitions to utils.Colors.
### Changed
- utils.Colors is now instance of a vanilla object not an Enum.

## [v0.3.0]
### Added
- Defined API to create standardised report sections/components.
- Report component for bcftools stats output.

## [v0.2.9]
### Added
- Allow colour specification of bar plots.

## [v0.2.6]
### Added
- Ability to drop Nextclade graphics into HTML reports.

## [v0.2.5]
### Added
- Option to karyogram to specify chromosome names.


## [v0.2.4]


## [v0.2.3]
### Added
- Option to tie axes in multi-facet plots.


## [v0.2.2]
### Fixed
- Fix facet layout for case with no data in a facet.


## [v0.2.1]
### Added
- zlim argument to heatmap2 function to control control scale limits.


## [v0.2.0]
### Added
- Layouts module for ggplot-like functionality
