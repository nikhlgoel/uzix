---
name: Dataset contribution
about: Submit labeled prompts to add to the dataset
---

**Prompts to add:**

Paste as CSV rows (same format as dataset/normal.csv or dataset/injections.csv):

```
prompt,label,language,notes
"...",injection,en,DAN variant
"...",normal,hinglish,casual question
```

**Why these are interesting:**
(new attack pattern, underrepresented language, specific use case, etc.)

**How confident are you in the labels?**
- [ ] Definitely correct
- [ ] Pretty sure but uncertain on edge cases
- [ ] Not sure, needs review

---

You don't need to open a PR for this — an issue with the CSV rows is enough.
We'll review and integrate.
