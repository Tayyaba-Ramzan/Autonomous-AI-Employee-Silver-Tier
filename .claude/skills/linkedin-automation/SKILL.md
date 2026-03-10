---
name: linkedin-automation
description: |
  Automate LinkedIn posting to generate business leads and engagement. Creates business-related
  posts, schedules content, manages approval workflow, and tracks engagement. Use when creating
  LinkedIn content or managing social media presence.
---

# LinkedIn Automation

Automate LinkedIn posting and engagement for business development.

## When to Use

- Generate LinkedIn posts about business activities
- Schedule content for optimal engagement
- Create approval requests for social posts
- Post approved content via Playwright browser automation
- Track post performance and engagement

## Workflow

### 1. Generate Post Ideas

Based on business activities, create posts about:
- New projects or milestones
- Industry insights
- Success stories
- Tips and best practices
- Company updates
- Thought leadership

### 2. Draft LinkedIn Post

Create a compelling post following LinkedIn best practices:

```markdown
---
type: linkedin_post
status: draft
created: 2026-03-09T10:00:00Z
scheduled_for: 2026-03-10T09:00:00Z
category: business_update
---

## Post Content

[Your post content here - 1-3 paragraphs]

Key points:
- Hook in first line
- Value proposition
- Call to action

## Hashtags

#BusinessDevelopment #AI #Automation #Productivity

## Media

- [ ] Image/graphic attached
- [ ] Link preview checked
- [ ] Alt text added

## Target Audience

Entrepreneurs, business owners, tech professionals

## Expected Outcome

Generate 50+ impressions, 5+ engagements, 1-2 leads
```

### 3. Create Approval Request

All LinkedIn posts require human approval:

```markdown
---
type: approval_request
action: linkedin_post
created: 2026-03-09T10:00:00Z
expires: 2026-03-10T09:00:00Z
status: pending
---

## LinkedIn Post Draft

[Post content here]

## Context

This post highlights our recent project success and positions us as experts
in AI automation. It's designed to attract potential clients interested in
similar solutions.

## Hashtags

#BusinessDevelopment #AI #Automation #Productivity

## Posting Schedule

Optimal time: Monday 9:00 AM (high engagement window)

## Approval Instructions

- **To Approve:** Move this file to `/Approved` folder
- **To Reject:** Move this file to `/Rejected` folder with reason
- **To Edit:** Modify the post content above and leave in this folder

## Risk Assessment

- Medium visibility: Public post on professional network
- Brand representation: Reflects company values and expertise
- Compliance: No sensitive information disclosed
```

### 4. Post to LinkedIn (After Approval)

Use Playwright browser automation to post:

```bash
# Start Playwright server
bash .claude/skills/browsing-with-playwright/scripts/start-server.sh

# Navigate to LinkedIn
python3 .claude/skills/browsing-with-playwright/scripts/mcp-client.py call \
  -u http://localhost:8808 -t browser_navigate \
  -p '{"url": "https://www.linkedin.com"}'

# Get page snapshot to find post button
python3 .claude/skills/browsing-with-playwright/scripts/mcp-client.py call \
  -u http://localhost:8808 -t browser_snapshot -p '{}'

# Click "Start a post" button
python3 .claude/skills/browsing-with-playwright/scripts/mcp-client.py call \
  -u http://localhost:8808 -t browser_click \
  -p '{"element": "Start a post", "ref": "e42"}'

# Type post content
python3 .claude/skills/browsing-with-playwright/scripts/mcp-client.py call \
  -u http://localhost:8808 -t browser_type \
  -p '{"element": "Post text area", "ref": "e15", "text": "Your post content here"}'

# Click Post button
python3 .claude/skills/browsing-with-playwright/scripts/mcp-client.py call \
  -u http://localhost:8808 -t browser_click \
  -p '{"element": "Post", "ref": "e50"}'

# Take screenshot for confirmation
python3 .claude/skills/browsing-with-playwright/scripts/mcp-client.py call \
  -u http://localhost:8808 -t browser_take_screenshot \
  -p '{"type": "png", "fullPage": false}'
```

### 5. Log and Track

After posting:
- Log post to `/Logs/linkedin_posts.md`
- Move approval request to `/Done`
- Update Dashboard with post count
- Schedule follow-up to check engagement

## LinkedIn Post Best Practices

### Content Structure

1. **Hook (First Line):** Grab attention immediately
2. **Value:** Provide insights, tips, or stories
3. **Call to Action:** What should readers do next?

### Optimal Posting Times

- **Monday-Friday:** 9:00 AM, 12:00 PM, 5:00 PM
- **Avoid:** Weekends, late nights
- **Best days:** Tuesday, Wednesday, Thursday

### Content Types That Perform Well

- Personal stories and lessons learned
- Industry insights and trends
- How-to guides and tips
- Company milestones and wins
- Thought-provoking questions
- Visual content (images, infographics)

### Hashtag Strategy

- Use 3-5 relevant hashtags
- Mix popular and niche tags
- Research trending hashtags in your industry
- Create branded hashtags for campaigns

## Post Templates

### Project Success Story

```
Just wrapped up an exciting project that [outcome/result]. 🎉

The challenge: [Brief description of problem]

Our approach: [How you solved it]

The result: [Measurable outcomes]

Key takeaway: [Lesson learned]

What's your experience with [topic]? Drop a comment below!

#BusinessDevelopment #ProjectManagement #Success
```

### Industry Insight

```
Here's something I've noticed in [industry]: [Observation]

Why this matters:
→ [Point 1]
→ [Point 2]
→ [Point 3]

The opportunity: [What this means for businesses]

Are you seeing this trend too? Let's discuss in the comments.

#Industry #Trends #BusinessStrategy
```

### Tip/How-To

```
3 ways to [achieve desired outcome]:

1. [Tip 1 with brief explanation]
2. [Tip 2 with brief explanation]
3. [Tip 3 with brief explanation]

Bonus tip: [Additional insight]

Which one will you try first?

#Tips #HowTo #Productivity
```

## Engagement Strategy

After posting:
- Respond to comments within 2 hours
- Thank people for engaging
- Ask follow-up questions
- Share post to relevant groups
- Tag relevant connections (sparingly)

## Content Calendar

Maintain a posting schedule:
- **Monday:** Industry insights
- **Wednesday:** Project updates
- **Friday:** Tips and how-tos

Frequency: 2-3 posts per week

## Compliance and Safety

**Never post:**
- Confidential client information
- Sensitive financial data
- Controversial political opinions
- Unverified claims or statistics
- Negative comments about competitors

**Always:**
- Get approval before posting
- Verify facts and figures
- Use professional language
- Respect intellectual property
- Follow LinkedIn's terms of service

## Error Handling

If posting fails:
1. Take screenshot of error
2. Log error to `/Logs/errors.md`
3. Move approval back to `/Pending_Approval` with note
4. Alert user via Dashboard
5. Do not retry automatically

## Metrics to Track

- Impressions
- Engagements (likes, comments, shares)
- Profile views
- Connection requests
- Direct messages
- Click-through rates (if links included)

Log metrics to `/Accounting/linkedin_metrics.md`

## Key Principles

1. **Quality over quantity** - Post valuable content, not filler
2. **Always get approval** - Never post without human review
3. **Be authentic** - Share genuine insights and experiences
4. **Engage with audience** - Respond to comments promptly
5. **Track performance** - Learn what resonates with your audience
6. **Stay professional** - Maintain brand reputation

## File Naming Conventions

- Post drafts: `LINKEDIN_POST_[topic]_[date].md`
- Approval requests: `APPROVAL_LINKEDIN_[topic]_[date].md`
- Logs: `LOG_LINKEDIN_[date].md`
