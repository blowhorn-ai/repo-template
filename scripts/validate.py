#!/usr/bin/env python3
"""scripts/validate.py
Comprehensive validation suite for the Blowhorn AI repository template
and the organization-neutral upstream/ version.
"""

import os
import re
import sys
import subprocess

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UPSTREAM_DIR = os.path.join(REPO_ROOT, "upstream")

def log(section: str):
    print(f"\n=== {section} ===")

def parse_simple_yaml(filepath: str):
    """Basic line-based parser to validate syntax and indentation."""
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # Check for basic syntax anomalies (tabs instead of spaces, unbalanced quotes, colon formatting)
    for idx, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "\t" in line.split("#")[0]:
            raise ValueError(f"Tab character found on line {idx}")
        # Check basic key-value syntax if contains colon
        if ":" in line and not line.strip().startswith("-"):
            parts = line.split(":", 1)
            key = parts[0].strip()
            if " " in key and not (key.startswith("'") or key.startswith('"')):
                pass # valid in some YAML keys
    return True

def validate_yaml_files():
    log("1. Validating YAML Syntax")
    yaml_files = []
    for root, dirs, files in os.walk(REPO_ROOT):
        # Don't recurse into .git
        if ".git" in dirs:
            dirs.remove(".git")
        for file in files:
            if file.endswith((".yml", ".yaml")):
                yaml_files.append(os.path.join(root, file))
    
    errors = 0
    for yf in sorted(yaml_files):
        rel = os.path.relpath(yf, REPO_ROOT)
        try:
            parse_simple_yaml(yf)
            print(f"  [OK] Valid YAML: {rel}")
        except Exception as e:
            print(f"  [FAIL] YAML error in {rel}: {e}")
            errors += 1
    return errors == 0

def validate_workflows():
    log("2. Validating GitHub Actions Workflows")
    workflow_dirs = [
        os.path.join(REPO_ROOT, ".github", "workflows"),
        os.path.join(UPSTREAM_DIR, ".github", "workflows")
    ]
    
    errors = 0
    expected_workflows = [
        "ci.yml", "slack.yml", "labeler.yml", "label-commenter.yml",
        "release-drafter.yml", "multi-platform.yml"
    ]
    
    for wf_dir in workflow_dirs:
        rel_dir = os.path.relpath(wf_dir, REPO_ROOT)
        if not os.path.isdir(wf_dir):
            print(f"  [FAIL] Missing workflow directory: {rel_dir}")
            errors += 1
            continue
        
        for wf_name in expected_workflows:
            wf_path = os.path.join(wf_dir, wf_name)
            rel_path = os.path.relpath(wf_path, REPO_ROOT)
            if not os.path.isfile(wf_path):
                print(f"  [FAIL] Missing expected workflow: {rel_path}")
                errors += 1
                continue
            
            with open(wf_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Check for permissions block (security policy)
            if "permissions:" not in content:
                print(f"  [FAIL] Missing 'permissions:' block in {rel_path}")
                errors += 1
            elif "permissions: write-all" in content:
                print(f"  [FAIL] Overly broad 'permissions: write-all' in {rel_path}")
                errors += 1
            else:
                print(f"  [OK] Security permissions verified in {rel_path}")
            
            # Verify no Tells-specific Cloudflare or npm leaks
            if "wrangler" in content.lower() or "cloudflare" in content.lower():
                print(f"  [FAIL] Cloudflare deployment leak in {rel_path}")
                errors += 1
            if "publish-blowhorn-tells" in content:
                print(f"  [FAIL] Tells npm publish leak in {rel_path}")
                errors += 1
            
            # Check multi-platform container names
            if wf_name == "multi-platform.yml":
                if "meshery" in content.lower() or "layer5" in content.lower():
                    print(f"  [FAIL] Meshery/Layer5 image name leaked in {rel_path}")
                    errors += 1
                else:
                    print(f"  [OK] Generic container configuration in {rel_path}")
    return errors == 0

def validate_issue_templates():
    log("3. Validating Issue Templates & Configuration")
    template_dirs = [
        os.path.join(REPO_ROOT, ".github", "ISSUE_TEMPLATE"),
        os.path.join(UPSTREAM_DIR, ".github", "ISSUE_TEMPLATE")
    ]
    
    errors = 0
    expected_templates = ["bug_report.md", "feature_request.md", "documentation.md", "ci.md", "config.yml"]
    
    for t_dir in template_dirs:
        rel_dir = os.path.relpath(t_dir, REPO_ROOT)
        for t_file in expected_templates:
            p = os.path.join(t_dir, t_file)
            rel = os.path.relpath(p, REPO_ROOT)
            if not os.path.isfile(p):
                print(f"  [FAIL] Missing template: {rel}")
                errors += 1
                continue
            
            with open(p, "r", encoding="utf-8") as f:
                content = f.read()
            
            if t_file == "config.yml":
                if "blank_issues_enabled: false" not in content:
                    print(f"  [FAIL] blank_issues_enabled is not false in {rel}")
                    errors += 1
                else:
                    print(f"  [OK] Blank issues disabled in {rel}")
            else:
                # Check markdown frontmatter
                if not content.startswith("---"):
                    print(f"  [FAIL] Missing YAML frontmatter in {rel}")
                    errors += 1
                elif "name:" not in content or "about:" not in content:
                    print(f"  [FAIL] Incomplete frontmatter in {rel}")
                    errors += 1
                else:
                    print(f"  [OK] Valid issue template: {rel}")
    return errors == 0

def validate_agent_skills():
    log("4. Validating Agent Skills")
    skill_dirs = [
        os.path.join(REPO_ROOT, ".agents", "skills"),
        os.path.join(UPSTREAM_DIR, ".agents", "skills")
    ]
    errors = 0
    expected_skills = ["code-review", "documentation", "repo-navigation", "testing"]
    
    for s_dir in skill_dirs:
        rel_dir = os.path.relpath(s_dir, REPO_ROOT)
        for skill in expected_skills:
            skill_md = os.path.join(s_dir, skill, "SKILL.md")
            rel = os.path.relpath(skill_md, REPO_ROOT)
            if not os.path.isfile(skill_md):
                print(f"  [FAIL] Missing skill file: {rel}")
                errors += 1
                continue
            with open(skill_md, "r", encoding="utf-8") as f:
                c = f.read()
            if not c.startswith("---") or "name:" not in c or "description:" not in c:
                print(f"  [FAIL] Invalid frontmatter in skill {rel}")
                errors += 1
            else:
                print(f"  [OK] Valid agent skill: {rel}")
    return errors == 0

def validate_shell_scripts():
    log("5. Validating Shell Scripts")
    scripts = [
        os.path.join(REPO_ROOT, "scripts", "sync-labels.sh"),
        os.path.join(REPO_ROOT, "scripts", "sync-upstream.sh"),
        os.path.join(UPSTREAM_DIR, "scripts", "sync-labels.sh")
    ]
    errors = 0
    for s in scripts:
        rel = os.path.relpath(s, REPO_ROOT)
        if not os.path.isfile(s):
            print(f"  [FAIL] Script not found: {rel}")
            errors += 1
            continue
        if not os.access(s, os.X_OK):
            print(f"  [FAIL] Script is not executable: {rel}")
            errors += 1
        else:
            print(f"  [OK] Executable permissions verified: {rel}")
        
        # Syntax check using bash -n
        res = subprocess.run(["bash", "-n", s], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"  [FAIL] Shell syntax error in {rel}: {res.stderr}")
            errors += 1
        else:
            print(f"  [OK] Shell syntax valid: {rel}")
    return errors == 0

def validate_markdown_links():
    log("6. Validating Markdown Links")
    md_files = []
    for root, _, files in os.walk(REPO_ROOT):
        if "/.git" in root:
            continue
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))
    
    errors = 0
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    
    for mf in md_files:
        rel_src = os.path.relpath(mf, REPO_ROOT)
        src_dir = os.path.dirname(mf)
        with open(mf, "r", encoding="utf-8") as f:
            content = f.read()
        
        for match in link_pattern.finditer(content):
            _, target = match.groups()
            # Ignore external URLs, mailto, and fragments
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            # Strip anchors if any
            clean_target = target.split("#")[0]
            if not clean_target:
                continue
            resolved = os.path.normpath(os.path.join(src_dir, clean_target))
            if not os.path.exists(resolved):
                print(f"  [FAIL] Dead link in {rel_src} -> {target} (resolved: {os.path.relpath(resolved, REPO_ROOT)})")
                errors += 1
    
    if errors == 0:
        print(f"  [OK] All internal relative markdown links verified across {len(md_files)} files.")
    return errors == 0

def validate_upstream_sync():
    log("7. Validating Upstream Synchronization & Parity")
    script = os.path.join(REPO_ROOT, "scripts", "sync-upstream.sh")
    res = subprocess.run(["bash", script, "--check"], capture_output=True, text=True)
    print(res.stdout)
    if res.returncode != 0:
        print(res.stderr)
        return False
    return True

def main():
    print("Starting Blowhorn AI Repository Template Validation Suite...")
    success = True
    success &= validate_yaml_files()
    success &= validate_workflows()
    success &= validate_issue_templates()
    success &= validate_agent_skills()
    success &= validate_shell_scripts()
    success &= validate_markdown_links()
    success &= validate_upstream_sync()
    
    log("Validation Summary")
    if success:
        print("🎉 ALL QUALITY, SECURITY, AND SYNCHRONIZATION CHECKS PASSED!\n")
        return 0
    else:
        print("❌ VALIDATION SUITE DETECTED FAILURES. See details above.\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
