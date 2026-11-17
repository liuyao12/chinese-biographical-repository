/** A source-bound editorial heading choice; never a tenure or life-period claim. */
export function profileTitlePreference(profile) {
  const choice = profile?.default_profile_title;
  if (!choice || choice.status !== 'editorial_provisional'
      || choice.temporal_claim !== 'none' || typeof choice.title !== 'string'
      || !choice.title.trim()) return null;
  return choice;
}
