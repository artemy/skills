# artemy-skills

Personal collection of Claude skills, packaged as a Claude Code plugin.

```
.claude-plugin/
├── marketplace.json    # catalog: this repo offers one plugin, artemy-skills
└── plugin.json         # the plugin itself
skills/
└── <SKILL-NAME>/    # one directory per skill
    ├── SKILL.md        # required: frontmatter (name, description) + instructions
    └── scripts/        # optional helper scripts
scripts/
└── validate.py         # frontmatter checks for every skill
```

## Install

```bash
claude plugin marketplace add artemy/skills
claude plugin install artemy-skills@artemy
```

Skills land namespaced as `artemy-skills:<SKILL-NAME>`.

Updating: `claude plugin marketplace update artemy`.

To develop against a local checkout instead, point the marketplace at the
working copy — `claude plugin marketplace add /Some/working/dir/skills` —
or skip the plugin machinery entirely and symlink a single skill:

```bash
ln -s /Some/working/dir/skills/recipe-rewriter \
      ~/.claude/skills/recipe-rewriter
```

## Adding a skill

1. Create `skills/<skill-name>/SKILL.md` with frontmatter:

   ```markdown
   ---
   name: skill-name
   description: What it does and, crucially, when Claude should reach for it.
   ---

   # Skill Name

   Instructions...
   ```

   `name` must match the directory name. `description` is the only thing Claude
   sees before deciding to load the skill, so it should name concrete triggers —
   the phrasings and situations that should activate it — not just the topic.

2. Put helper scripts in `skills/<skill-name>/scripts/`, referenced by relative
   path from SKILL.md.
3. Run `python3 scripts/validate.py`.

## Skills

| Skill | Description |
|---|---|
| `recipe-rewriter` | Rewrites recipes from any source into one compact Russian-language format: ingredients, numbered steps, notes, metric units, source link. |

## License

MIT — see [LICENSE](LICENSE).
