# Friendsloop: tiny online games with friends

## Design target

Here, **friendsloop** means a game whose replay value comes mainly from the people playing: shared tension → a funny reveal → blame, celebration, or revenge → immediate rematch. This is a working interpretation, not a formal genre definition.

**Constraints:** online multiplayer, one core action per concept, text or simple shapes, minimal authored content, and a plausible paid Steam release. All ideas below work with private groups; none should depend on a healthy public matchmaking population at launch.

**Default scope:** 3–6 friends, 5–10-minute matches, room codes, rematches, and external voice chat. Some concepts support two players. No built-in voice, accounts, progression, inventory, or level editor in the first version.

A single mechanic does not eliminate multiplayer engineering. Connection handling, clear feedback, onboarding, and reliable rematches are part of the minimum product.

## Ranking

Scores are editorial estimates, not playtest or market evidence. Weighted score: social fun 35%, production ease 30%, mechanical simplicity 20%, Steam product potential 15%. Each component is rated 1–5; higher is better. Production ease includes networking, content, and UI—not just gameplay code.

| Rank | Concept | Mode / players | Only core action | Fun | Ease | Simple | Steam | Weighted / 5 |
|---|---|---|---|---:|---:|---:|---:|---:|
| 1 | **One More Floor** | Push-your-luck PvP, 2–6 | Stay or leave | 5 | 5 | 5 | 4 | 4.85 |
| 2 | **The Last Volunteer** | Co-op/social dilemma, 3–6 | Volunteer or abstain | 5 | 5 | 5 | 3 | 4.70 |
| 3 | **Claim / Call** | Bluffing PvP, 2–6 | Claim a count or call a bluff | 5 | 4 | 4 | 4 | 4.35 |
| 4 | **Say the Same Thing** | Co-op, 2–6 | Submit one word | 4 | 5 | 5 | 2 | 4.20 |
| 5 | **Not That Door** | Prediction PvP, 3–8 | Pick a door | 4 | 5 | 5 | 2 | 4.20 |
| 6 | **Signal Lost** | Co-op, 2–6 | Press your button once | 4 | 4 | 5 | 3 | 4.05 |
| 7 | **The Quiet Auction** | Economic PvP, 3–6 | Submit a bid | 4 | 4 | 4 | 4 | 4.00 |
| 8 | **One-Line Alibi** | Social deduction, 4–8 | Submit one sentence | 5 | 3 | 3 | 4 | 3.85 |
| 9 | **Pass the Problem** | Hot-potato PvP, 3–8 | Pass to another player | 4 | 3 | 5 | 3 | 3.75 |
| 10 | **Don't Be the Last** | Timing PvP, 2–6 | Bank your score | 4 | 3 | 5 | 3 | 3.75 |
| 11 | **Borrowed Eyes** | Communication co-op, 2–4 | Choose left or right | 4 | 3 | 4 | 3 | 3.55 |
| 12 | **Shared Cursor** | Coordination co-op, 2–4 | Hold a direction | 4 | 2 | 4 | 4 | 3.40 |

Ties favor the concept with less technical or content uncertainty. Lower-ranked ideas are not necessarily less fun; they are worse fits for *easy production*.

---

## 1. One More Floor — recommended first prototype

**Pitch:** Your friends share a suspicious elevator. Every floor adds loot. Everyone secretly chooses whether to leave with their share or stay for the next floor. Eventually, the elevator fails.

- **Mechanic:** simultaneous `STAY / LEAVE` decisions. Leaving ends your participation in that trip, not the match.
- **Rules:** each safe floor adds coins to a shared pot. At a decision, departing players split the pot equally; any remainder stays aboard. If nobody leaves, the pot grows. Staying players risk losing everything still aboard. Failure odds increase with depth and are visible. Banked coins are safe. Most coins after five trips wins.
- **Friendsloop:** “We both leave now” → one friend stays → the survivor gets greedy → catastrophic reveal → revenge next trip.
- **Presentation:** elevator floor number, player initials, a coin counter, two buttons, warning lights, and a satisfying failure sound. ASCII could handle nearly all of it.
- **Implementation:** authoritative room state machine: safe floor → private choices → simultaneous reveal → payout → next-floor risk roll. Only a handful of small network messages per round. No physics or fast synchronization.
- **Production trap:** early leavers may wait too long. Limit trips to roughly a minute and let them spectate the choices and impending disaster. Test splitting the whole pot carefully; it may create overly obvious decisions.
- **Steam angle:** an immediately legible premise and dramatic reveals. Needs excellent sound and pacing to feel like a product rather than a UI exercise. Do not rely on the provisional name being available.

**Prototype question:** Do friends negotiate and accuse each other without prompts? If everyone silently follows a fixed exit strategy, adjust the payout/risk curve before adding features.

## 2. The Last Volunteer

**Pitch:** The ship survives only if exactly one person presses the emergency button. Everyone swears someone else should do it.

- **Mechanic:** secretly volunteer or abstain, then reveal together.
- **Rules:** exactly one volunteer saves the round and pays one personal energy. Zero or multiple volunteers cost the team one hull. Players with no energy cannot volunteer. Survive eight emergencies before losing three hull. Energy budgets are private, so verbal claims matter.
- **Friendsloop:** coordination → promises → two heroes or zero heroes → collective outrage.
- **Presentation:** a terminal, hull indicator, energy bars visible only to their owner, and a dramatic list of who pressed.
- **Implementation:** almost identical networking to #1. Generate starting energy budgets with enough total energy to make survival possible; reveal everyone’s remaining energy at the end.
- **Production trap:** honest groups can establish a rotation and solve it. This is the central design risk, not a minor balance issue. Private budgets alone may not prevent it. Test before building extra scenarios.
- **Steam angle:** strong party moment, but potentially too thin for a standalone paid game. Better as a very small release or later companion mode if playtesting supports it.

## 3. Claim / Call

**Pitch:** Everyone receives a tiny private handful of symbols. How many skulls exist around the table? Your friend says seven. Are they lying?

- **Mechanic:** raise the current claim or call it false.
- **Rules:** each player gets five hidden symbols. Claims name a symbol and a total count across all players; each new claim must increase the count. Calling reveals everything. An incorrect claimant or caller loses a point. Redeal every round; nobody is eliminated. Highest score after a fixed number of rounds wins.
- **Friendsloop:** absurd confidence → reluctant escalation → a call → table-wide reveal.
- **Presentation:** symbol tiles, a claim log, player portraits made from initials, and large reveal animations.
- **Implementation:** turn-based server with private hands, public claims, and a short turn timer. Keep hidden hands off other clients until the reveal.
- **Production trap:** familiar bluffing-dice territory. Easy to understand, harder to distinguish commercially. Count limits and forced calls need explicit rules.
- **Steam angle:** reliable social structure, but create original branding, graphics, wording, and presentation rather than cloning a particular product.

## 4. Say the Same Thing

**Pitch:** Two random words appear. Everyone types the word that connects them. Can your group converge on the same answer?

- **Mechanic:** submit one word secretly.
- **Rules:** reveal submissions together. Full agreement wins. Otherwise, two different submissions become the next seed pair. Converge within six rounds. Players must not say or signal their intended answer before the reveal.
- **Friendsloop:** startling associations → laughter → “I know how your brain works now” → another attempt.
- **Presentation:** large typography and branching word trails.
- **Implementation:** tiny turn-based protocol; trim whitespace and normalize case. Explicitly show why answers did or did not match. Start with a modest, manually reviewed seed list.
- **Production trap:** alternate spellings, inflections, languages, and deliberate off-topic convergence. Avoid semantic AI matching: it adds cost and unpredictable judgments.
- **Steam angle:** exceptionally cheap prototype, weak standalone differentiation. Language support requires actual testing, not just translated buttons.

## 5. Not That Door

**Pitch:** Three doors. Pick one nobody else picks, and you score.

- **Mechanic:** secretly choose a door.
- **Rules:** a door occupied by exactly one player awards its posted points. Crowded doors award nothing. For larger groups, increase the door count. Play ten quick rounds with changing, publicly visible door values.
- **Friendsloop:** threats and promises → everyone chooses the “obvious” safe option → nobody scores.
- **Presentation:** chunky numbered doors and a simultaneous crowd reveal.
- **Implementation:** simplest possible choice/reveal state machine. Door values come from a small, bounded random generator.
- **Production trap:** silent random selection may perform as well as social reads. Test whether conversation actually improves the experience.
- **Steam angle:** excellent mode-sized idea, questionable full product. Sell only if the social loop proves unusually strong.

## 6. Signal Lost

**Pitch:** Your crew must send one synchronized pulse—but everyone receives a different piece of the countdown.

- **Mechanic:** press once per attempt.
- **Rules:** each player briefly sees a different countdown cue toward the same target time. Cues then disappear. The team scores for both closeness to the target and closeness to one another. Voice coordination is allowed.
- **Friendsloop:** improvised countdown → somebody panics → timing chart exposes the culprit.
- **Presentation:** terminal clocks, radio static, and a post-round timeline.
- **Implementation:** server schedules a future target; clients estimate server-clock offset. Start with generous scoring windows and test across real internet connections.
- **Production trap:** network delay and differing audio/display latency can feel like player error. Avoid millisecond-precision claims and ranked competition.
- **Steam angle:** sound-led atmosphere could make simple visuals compelling, but accessibility needs visual alternatives to audio cues.

## 7. The Quiet Auction

**Pitch:** Bid your limited money for mysterious junk while convincing friends to waste theirs.

- **Mechanic:** submit one sealed bid, including zero to pass.
- **Rules:** everyone begins with 30 credits for six auctions. Items have public point values. Highest bidder pays and receives the item; tied highest bids cancel the sale and nobody pays. Most item points wins, with remaining money as the tiebreaker.
- **Friendsloop:** fake enthusiasm → an enormous overbid → a bargain nobody saw coming.
- **Presentation:** item names, tiny icons, and a receipt-style results screen.
- **Implementation:** turn-based economy with server-side balance validation. A few dozen humorous item names are sufficient; their point values can vary independently.
- **Production trap:** needs payout and money tuning. Avoid item powers initially—they turn a tiny game into a content and rules project.
- **Steam angle:** more strategic substance than several higher-ranked ideas while retaining almost entirely text-based production.

## 8. One-Line Alibi

**Pitch:** Everyone knows the secret location except one impostor. Each player writes a single sentence explaining what they were doing there.

- **Mechanic:** write one short alibi; a separate accusation vote resolves the round. **This is deliberately a weaker fit for the one-mechanic constraint.**
- **Rules:** reveal alibis together, discuss briefly, then vote. The group wins if a strict majority identifies the impostor; otherwise the impostor wins.
- **Friendsloop:** suspicious wording → improvised defense → a friend reads far too much into one sentence.
- **Presentation:** case-file cards and a typewriter reveal.
- **Implementation:** hidden-role assignment, private prompt delivery, submissions, timer, and voting. Needs a curated location bank and repetition control.
- **Production trap:** content quality, language dependence, and larger minimum group. Public rooms introduce user-content moderation work.
- **Steam angle:** clear social appeal, but a crowded concept space and more writing work than the simpler choices.

## 9. Pass the Problem

**Pitch:** A cursed package circulates among your friends. It will explode. You may send it to anyone—except whoever just sent it to you.

- **Mechanic:** click a recipient while holding the package.
- **Rules:** a hidden server timer determines detonation. Transfers have a brief cooldown; immediate return is forbidden. The holder loses one point when it bursts. Nobody is eliminated.
- **Friendsloop:** targeted bullying → alliances → a perfectly timed betrayal.
- **Presentation:** player names arranged around a parcel with increasingly ominous effects.
- **Implementation:** authoritative ownership, transfer validation, and timer resolution. Client animations follow server results.
- **Production trap:** latency at detonation and dogpiling one player. Keep rounds casual, provide readable transfer feedback, and avoid claiming competitive timing fairness.
- **Steam angle:** energetic clips, but uncertain depth. A weaker low-risk production choice than turn-based games.

## 10. Don't Be the Last

**Pitch:** A communal score climbs. Cash out whenever you want—but the last person still waiting gets nothing.

- **Mechanic:** press `BANK` once per round.
- **Rules:** bank the displayed value when the server accepts your press. When only one player remains, their score becomes zero and the round ends. If multiple players remain at the time limit, those players get zero. Five rounds per match.
- **Friendsloop:** fake countdowns → someone flinches → a sudden cascade of panic.
- **Presentation:** one enormous number and player status lights.
- **Implementation:** server clock, timestamped events, and an explicit tie policy. Batch presses into short intervals and allow shared placement within an interval rather than pretending all close inputs have an indisputable order.
- **Production trap:** ping can decide outcomes. Also, repeated immediate banking may drain all the tension.
- **Steam angle:** exceptionally clear trailer, but the game must prove it stays fun beyond the first few matches.

## 11. Borrowed Eyes

**Pitch:** Guide a tiny rover through binary junctions. You choose the path, but only your friends can see the warning signs.

- **Mechanic:** the active driver selects left or right; the driver rotates after each junction.
- **Rules:** other players receive complementary clues identifying the safe exit. They explain them verbally. Reach the destination before taking three wrong turns.
- **Friendsloop:** ambiguous instructions → confident wrong turn → arguments over what “the other left” means.
- **Presentation:** ASCII junctions, two arrow buttons, and private clue panels.
- **Implementation:** turn-based, role-specific views. Start with a handful of tested clue templates; generate only combinations with a unique valid answer.
- **Production trap:** puzzle generation and clue writing are the actual workload. A completely straightforward clue system may become trivial.
- **Steam angle:** appealing co-op identity, but less content-free than it first appears.

## 12. Shared Cursor

**Pitch:** Everyone controls the same dot. Nobody agrees where it should go.

- **Mechanic:** hold a direction; the game averages all players’ input vectors.
- **Rules:** guide the dot through a corridor to the finish before time expires. Touching a wall resets to the latest checkpoint.
- **Friendsloop:** competing instructions → accidental success → increasingly ridiculous leadership arrangements.
- **Presentation:** vector lines, one circle, a timer, and visible input arrows.
- **Implementation:** fixed-step authoritative movement, networked input state, and interpolated rendering. Begin with a few handmade corridors, not procedural generation.
- **Production trap:** movement feel, latency, collision behavior, and level design. A designated leader may reduce everyone else to following instructions.
- **Steam angle:** strongest immediate visual motion here, but furthest from the easy-production brief.

---

## Recommended technology

### Default: Godot + a small authoritative room server

For **One More Floor**, use **Godot 4 with GDScript** for a lightweight desktop UI client. A small TypeScript/Node.js WebSocket service owns rooms, choices, random outcomes, scores, and reconnection state. If keeping one language matters more, evaluate a headless Godot server instead; choose one backend, not both.

Why this default:

- Text, buttons, simple animation, and audio need no heavy engine features.
- Turn-based play tolerates ordinary network latency.
- A central server makes room codes straightforward and avoids player router configuration.
- The backend can stay small: create/join room, start match, submit action, reveal, reconnect, rematch.

**Tradeoff:** server hosting, deployment, abuse controls, monitoring, and ongoing availability are real obligations. Low message volume does not mean zero operating cost. Test concurrency before estimating capacity.

**Do not build a generic multiplayer platform first.** Implement one game's state machine and a thin room layer.

### Where GDevelop fits

GDevelop is reasonable if visual scripting is your fastest way to prototype. Build the local rules/UI first, then validate its current multiplayer offerings, desktop export workflow, limits, pricing, and Steam integration path with a two-player internet test. Those details can change; this document does not assume a particular hosted feature or paid plan is available.

For a custom room server and tightly controlled hidden information, Godot plus a small coded backend is the more explicit architecture. If you already know JavaScript well, a web UI in a desktop wrapper is also viable, though it adds packaging and Steam integration decisions.

### Steam networking alternative

Steam lobbies plus Steam networking can provide Steam-native discovery/invites and potentially relay-backed connectivity, depending on the selected API and integration. They are not a substitute for authoritative game rules. Host-authoritative play can avoid a dedicated game backend, but requires a maintained engine integration and a policy for host departure.

For the smallest first release: **room codes + central server**, with Steam invites added only after a working integration spike. If avoiding recurring hosting is a hard requirement, evaluate the Steam-hosted-session approach before committing to the architecture.

## What makes this a Steam product, not just a prototype?

1. **Lead with the social hook.** A trailer should show decisions, betrayal, and consequences—not menus or networking setup.
2. **Start with one platform.** Windows first; add other operating systems only when you can test and support them.
3. **Make joining painless.** Copyable room codes, clear errors, a visible player list, and host-controlled start. Steam invites are desirable polish, not something room codes automatically provide.
4. **Respect private information.** Keep unrevealed choices and outcomes on the authority. Validate legal actions, room membership, and message size; do not trust the client.
5. **Handle interruption.** Rejoin tokens, bounded reconnect grace, and deterministic timeouts. For #1, timeout defaults to leaving; refunding or pausing a whole match would invite abuse.
6. **Polish the reveal.** Typography, readable color-independent status, adjustable audio, animation speed, and an excellent results screen matter more than asset volume.
7. **Be honest about the group requirement.** Clearly state minimum players, internet requirements, and whether every player needs a copy. Do not promise solo play or bots unless implemented.
8. **Keep launch scope private.** Public matchmaking creates queue-health and moderation problems. Room codes reduce exposure, but still need rate limits and basic host controls.
9. **Treat pricing as a test.** A low single-digit USD price could fit a deliberately small party game, but friends buying multiple copies creates friction. Assess value after playtests; neither low price nor Steam distribution guarantees demand.
10. **Verify current Steamworks requirements.** Budget for app submission costs, onboarding, store assets, build review, release timing, and any chosen SDK integration. Exact fees and policies are not verified here.

Steam Remote Play Together is a potential alternative for games built around shared local input, not a blanket replacement for these online designs. It is especially unsuitable as the default for per-player secret information. A free companion client or friend pass could reduce purchase friction, but adds product, integration, and support scope; defer it.

## Smallest sensible production plan

### Step 1 — validate the social loop without networking

Prototype **One More Floor** using a facilitator or a local rules script and private choice collection. Run it with at least three different groups. Use placeholder text and record:

- Do players understand the choices after one trip?
- Do they talk, negotiate, and react without prompting?
- Do early leavers remain interested?
- Does one strategy dominate?
- Do players voluntarily ask for a rematch?

As an initial gate—not a statistical proof—look for unprompted rematch requests from at least two groups. If the loop is flat, test **Claim / Call** before spending time on infrastructure.

### Step 2 — make one complete online match

Ship an internal build with create/join room, private choices, simultaneous reveal, scoring, timeouts, reconnect, and rematch. Test on separate home networks, including deliberate disconnects. Verify that hidden state is not broadcast early.

### Step 3 — turn that match into a small product

Add sound, animations, onboarding, settings, accessibility basics, installer/export testing, and Steam packaging. Then test purchase willingness with people outside your friend group. Keep extra modes out until the main loop earns repeat sessions.

For someone experienced with the chosen stack, a rules prototype may take days; a dependable online Steam release should be planned in weeks or longer, not as a weekend task. These are order-of-magnitude expectations, not a schedule commitment.

## Bottom line

**Build One More Floor first.** It offers the strongest combination of two-button simplicity, low networking complexity, almost no authored content, and naturally occurring betrayal.

**Keep Claim / Call as the fallback** if push-your-luck balancing does not produce interesting choices. **Use The Last Volunteer as a cheap experiment**, but reject it quickly if a fixed rotation solves the fun out of it.

The goal is not twelve miniature games. It is one tiny game that reliably makes a group say: **“Again—but this time, don't trust them.”**
