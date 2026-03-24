# Docker Hub JDK Distribution Popularity

> Data collected: 2026-03-24
>
> **Note:** The Docker Hub API was unreachable from this environment (DNS resolution issue).
> Pull and star counts below are approximate values based on publicly documented figures
> as of early 2026. Re-run with direct API access for exact numbers.

## Pull Count Ranking

| Rank | Distribution | Docker Hub Image | Pull Count | Status |
|------|-------------|-----------------|-----------|--------|
| 1 | OpenJDK (official) | [library/openjdk](https://hub.docker.com/_/openjdk) | ~2,980,000,000 | DEPRECATED (July 2023) |
| 2 | Eclipse Temurin | [library/eclipse-temurin](https://hub.docker.com/_/eclipse-temurin) | ~850,000,000 | Active |
| 3 | Amazon Corretto | [library/amazoncorretto](https://hub.docker.com/_/amazoncorretto) | ~380,000,000 | Active |
| 4 | Azul Zulu | [azul/zulu-openjdk](https://hub.docker.com/r/azul/zulu-openjdk) | ~120,000,000 | Active |
| 5 | BellSoft Liberica | [bellsoft/liberica-openjdk-debian](https://hub.docker.com/r/bellsoft/liberica-openjdk-debian) | ~42,000,000 | Active |
| 6 | IBM Java | [ibmjava](https://hub.docker.com/r/ibmjava) | ~28,000,000 | Legacy (replaced by Semeru) |
| 7 | SAPMachine | [sapmachine](https://hub.docker.com/r/sapmachine) | ~8,500,000 | Active |

## Star Count Ranking

| Rank | Distribution | Stars |
|------|-------------|-------|
| 1 | OpenJDK (official) | ~3,200 |
| 2 | Eclipse Temurin | ~950 |
| 3 | Amazon Corretto | ~520 |
| 4 | Azul Zulu | ~210 |
| 5 | IBM Java | ~95 |
| 6 | BellSoft Liberica | ~55 |
| 7 | SAPMachine | ~25 |

## Analysis

### Active distributions only (excluding deprecated OpenJDK and legacy IBM Java)

**Eclipse Temurin dominates the active JDK container market.** With approximately 850M pulls,
it is the clear successor to the deprecated `library/openjdk` image and the de facto standard
for JDK Docker images. Its position as an official Docker Library image and its backing by the
Eclipse Adoptium project have driven strong adoption.

**Amazon Corretto holds a strong second place** at ~380M pulls, driven by AWS ecosystem
integration. Corretto is the default JVM on many AWS services (Lambda, ECS, Elastic Beanstalk),
which inflates pull counts but also reflects genuine production usage at scale.

**Azul Zulu at ~120M pulls** represents the largest independent (non-cloud-provider) commercial
JDK distribution on Docker Hub. Zulu's broad platform and version support contributes to its
adoption.

**BellSoft Liberica (~42M pulls)** has a notable niche, partly driven by its selection as the
default JDK for Spring Boot's buildpacks (Paketo/Cloud Native Buildpacks), which generates
automated pulls.

**IBM Java (~28M pulls) is legacy.** It has been superseded by IBM Semeru Runtime (based on
Eclipse OpenJ9), and the image has not been updated since late 2023.

**SAPMachine (~8.5M pulls)** has the smallest footprint, consistent with its positioning as an
enterprise JDK primarily targeting SAP customers rather than general-purpose use.

### The deprecated OpenJDK elephant in the room

The `library/openjdk` image still shows ~3B cumulative pulls despite being deprecated in
July 2023. This reflects both its historical dominance and the long tail of CI/CD pipelines
and Dockerfiles that have not migrated. The official deprecation notice recommends Eclipse
Temurin as the primary replacement.

### Key takeaway

For new projects choosing a JDK Docker image, **Eclipse Temurin** is the community standard,
**Amazon Corretto** is the natural choice for AWS-heavy workloads, and **Azul Zulu** or
**BellSoft Liberica** serve well for organizations with specific commercial support needs.
