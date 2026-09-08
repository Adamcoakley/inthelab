/* ============================================================
   Personalisation, makes resource names unique per learner.
   The learner enters their name once. It's saved in their browser
   (localStorage) and swapped into every {{name}} / {{ns}} token
   on every page. No accounts, no database, no server.
   ============================================================ */

const KEY = 'bp_learner_name';

/** Turn a raw name into a safe resource prefix.
 *  "Adam"      -> "adam"
 *  "Chris B."  -> "chris-b"
 *  "José Díaz" -> "jose-diaz"
 *  Falls back to "learner" if empty. AWS-name-safe: lowercase, hyphens only. */
export function toSlug(raw) {
  if (!raw) return 'learner';
  const slug = raw
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '') // strip accents
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')  // non-alphanumeric -> hyphen
    .replace(/^-+|-+$/g, '')       // trim hyphens
    .slice(0, 20);                 // keep it short
  return slug || 'learner';
}

/** Possessive display form for prose: "adam" -> "adam's". */
export function toPossessive(slug) {
  if (!slug) return "the learner's";
  return slug.endsWith('s') ? `${slug}'` : `${slug}'s`;
}

export function getName() {
  try { return localStorage.getItem(KEY) || ''; } catch { return ''; }
}
export function setName(name) {
  try { localStorage.setItem(KEY, name); } catch {}
}

/** Replace tokens in a string:
 *   {{ns}}   -> slug prefix   (e.g. "adam"), use in resource names: {{ns}}-vpc
 *   {{name}} -> raw name      (e.g. "Adam"), use in friendly prose
 *   {{name's}} -> possessive  (e.g. "adam's"), use in prose about their resources */
export function applyTokens(text, rawName) {
  const name = rawName || 'there';
  const ns = toSlug(rawName);
  return text
    .replaceAll("{{name's}}", toPossessive(ns))
    .replaceAll('{{name}}', name)
    .replaceAll('{{ns}}', ns);
}

/** Walk the DOM and swap tokens inside any element marked data-personalize,
 *  plus update any element with [data-name-display]. Safe to call repeatedly. */
export function personalizePage() {
  const raw = getName();

  // swap tokens inside opted-in containers (keeps originals in data-tpl so we can re-run)
  document.querySelectorAll('[data-personalize]').forEach((el) => {
    if (!el.dataset.tpl) el.dataset.tpl = el.innerHTML;
    el.innerHTML = applyTokens(el.dataset.tpl, raw);
  });

  // fill in name displays (e.g. the header greeting)
  document.querySelectorAll('[data-name-display]').forEach((el) => {
    el.textContent = raw ? toSlug(raw) : 'not set';
  });

  // toggle a body flag so we can show/hide the "set your name" prompt
  document.body.dataset.hasName = raw ? 'yes' : 'no';
}
