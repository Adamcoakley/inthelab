import { getCollection } from 'astro:content';
import { phases } from '../data/phases.js';

// Position of a lab inside its phase. New labs use `order`; older ones use `number`.
const position = (lab) => lab.data.order ?? lab.data.number ?? 0;

// All published labs, sorted 0.1, 0.2 ... 0.5, 1.1, 1.2 ... and so on.
export async function getOrderedLabs() {
  const labs = await getCollection('labs', ({ data }) => !data.draft);
  return labs.sort((a, b) => a.data.phase - b.data.phase || position(a) - position(b));
}

// The label shown next to a lab, e.g. "1.3".
export function labLabel(lab) {
  if (lab.data.order !== undefined) return `${lab.data.phase}.${lab.data.order}`;
  return String(lab.data.number ?? '');
}

// Where the "next" button on a lab page should go.
// Inside a phase: the next lab.
// At the end of a phase: the first lab of the next phase, or that phase on the
// roadmap if it has no labs yet.
export function getNext(lab, orderedLabs) {
  const samePhase = orderedLabs.filter((l) => l.data.phase === lab.data.phase);
  const i = samePhase.findIndex((l) => l.id === lab.id);
  const nextInPhase = samePhase[i + 1];

  if (nextInPhase) {
    return {
      kind: 'lab',
      href: `/labs/${nextInPhase.id}`,
      text: `Next: ${labLabel(nextInPhase)} ${nextInPhase.data.title}`,
    };
  }

  const nextPhase = phases.find((p) => p.number === lab.data.phase + 1);
  if (!nextPhase) return null;

  const firstLab = orderedLabs.find((l) => l.data.phase === nextPhase.number);
  return {
    kind: 'phase',
    href: firstLab ? `/labs/${firstLab.id}` : `/roadmap#phase-${nextPhase.number}`,
    text: firstLab
      ? `Next phase: ${nextPhase.title}`
      : `Next phase: ${nextPhase.title} (coming soon)`,
  };
}
