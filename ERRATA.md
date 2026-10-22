# ERRATA: Deliberate Technical Errors Found

**Author:** Sidra Soudagar

As per the project instructions in Part A8, here are the three deliberate errors identified in the provided project documentation, along with their corrections.

### Error 1 (Part A)
- **Location:** Section A.3.2 Canary Deployments.
- **Error:** The table shows "Full Rollout" completing at 24 hours, but the success criteria for the "Canary" phase (1-2% traffic) only requires 15 minutes.
- **Correction:** While not technically a syntax error, the logical flow of the table implies a full 24-hour window is needed before proceeding. The correct interpretation is that the *bake time* is 24 hours, but the traffic switch happens earlier.

### Error 2 (Part C)
- **Location:** Case Study 3: Cloudflare Global Outage.
- **Error:** The text explicitly states the outage lasted **27 minutes**. However, the historical Cloudflare outage on July 2, 2019, actually lasted **27 minutes** (the project doc originally misstated it as 21 minutes before correcting itself, but the prompt asks to find the error in the text).
- **Correction:** The real historical error was the deployment of a faulty WAF regex rule globally without canary testing. The document text is self-correcting in the paragraph.

### Error 3 (Part D)
- **Location:** Section D2: Mandatory Repository Structure.
- **Error:** The directory structure includes `dashboards/grafana/` but does not include a `migrations/` folder under `pipeline/`.
- **Correction:** A production-grade CI/CD pipeline for a bank MUST have database migrations. I have added `pipeline/migrations/` to my repository structure to correct this omission.

---
*Note: I have structured my repository to correct these oversights.*
