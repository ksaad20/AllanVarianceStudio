## Description
<!-- Provide a clear and concise description of what this PR does -->

Fixes # (issue number)

## Type of Change
<!-- Mark the relevant option with an [x] -->
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring (no functional changes)
- [ ] Dependency update
- [ ] Test addition or improvement

## Changes Made
<!-- List the specific changes made in this PR -->
- 
- 
- 

## Testing
<!-- Describe the tests you ran and how to reproduce them -->
- [ ] Unit tests pass locally (`pytest`)
- [ ] Integration tests pass
- [ ] Manual testing performed (describe below)

**Test Configuration:**
- OS: 
- Python version: 
- NumPy version: 
- Pandas version: 

## Allan Variance Specific Checks
<!-- For AllanVarianceStudio, verify the following -->
- [ ] Allan variance calculations produce consistent results with reference data
- [ ] Noise parameter extraction (ARW, RRW, bias instability) is accurate
- [ ] Plot generation works for all supported file formats (`.bag`, `.csv`, `.feather`, `.mat`)
- [ ] YAML configuration output is valid and parseable
- [ ] No regression in computation performance for large datasets (>1M samples)

## Checklist
- [ ] My code follows the project's style guidelines (PEP 8)
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation (README, docstrings, etc.)
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published in downstream modules

## Data Compatibility
<!-- If this PR changes how data is processed or stored -->
- [ ] This change is backward compatible with existing input data files
- [ ] This change is backward compatible with existing YAML output files
- [ ] Migration guide provided (if breaking change)

## Screenshots / Output Examples
<!-- If applicable, add screenshots or example outputs to help explain your changes -->

## Related Issues
<!-- Link any related issues here -->
Closes #
Related to #

## Additional Notes
<!-- Add any other context or notes about the PR here -->
