# vajranow
# ⚡ VajraNow

## AI/ML-Based Thunderstorm & Lightning Nowcasting for Disaster Management

**Smart India Hackathon 2026 \| Problem Statement: SIH26072**\
**Theme:** Disaster Management\
**Organization:** Ministry of Earth Sciences (MoES)\
**Department:** India Meteorological Department (IMD)

> **Observe → Fuse → Predict → Explain → Alert**

VajraNow is a prototype decision-support platform for short-term
thunderstorm and lightning nowcasting. It is designed around the
SIH26072 requirement to combine atmospheric observations such as
**multiple Doppler weather radars, satellite observations, lightning
observations, and model/atmospheric data** and convert them into a
localized, time-aware risk estimate.

The current prototype demonstrates the complete user-facing workflow
with a lightweight ML model and controlled/demo inputs. The final target
architecture is designed to ingest real multi-source observations, align
them in space and time, run a spatiotemporal AI model, generate
probabilistic forecasts for the next 30--180 minutes, and translate
those forecasts into actionable disaster-management alerts.

------------------------------------------------------------------------

# 1. Problem Statement

## SIH26072

The official problem statement is:

> **"AIML based Nowcasting of thunderstorm and lightning using
> atmospheric observation including multiple radars, satellite,
> lightning and model data."**

The statement is under the **Disaster Management** theme and is
sponsored by the **Ministry of Earth Sciences / India Meteorological
Department**.

### What is nowcasting?

Nowcasting means forecasting a weather event over a **very short time
horizon**, generally minutes to a few hours.

For thunderstorms, the important questions are not only:

-   Is there a storm now?
-   Is it raining now?

The more useful disaster-management questions are:

-   **Where will the storm move?**
-   **Where can a new storm cell develop?**
-   **Will the storm intensify or decay?**
-   **Where is lightning risk increasing?**
-   **How much lead time is available for action?**

A thunderstorm can evolve much faster than a normal daily weather
forecast can communicate. Therefore, a system needs to continuously use
the latest observations and update the short-term risk estimate.

------------------------------------------------------------------------

# 2. Why This Problem Matters

Thunderstorms can produce several hazards at the same time:

-   Lightning
-   Heavy rain
-   Strong/gusty winds
-   Hail in some situations
-   Localized flash flooding
-   Damage to temporary structures
-   Disruption to transport and outdoor activities
-   Risk to farmers, construction workers and other people outdoors
-   Power and communication disruptions

For disaster management, **lead time matters**.

Consider two situations:

### Situation A: Reactive warning

A strong thunderstorm is already overhead.

The system detects it and a warning is issued.

People may have only a few minutes to react.

### Situation B: Short-term predictive warning

The system detects:

-   increasing radar reflectivity,
-   rapid cloud development,
-   increasing electrical activity,
-   atmospheric instability,
-   and movement toward a populated area.

VajraNow estimates that the thunderstorm probability will become high in
the next 30--60 minutes.

Now the control room can start preparing before the storm reaches the
vulnerable area.

That difference is the core motivation behind VajraNow.

------------------------------------------------------------------------

# 3. Our Solution in One Sentence

> **VajraNow fuses radar, satellite, lightning and atmospheric/model
> information with AI/ML to estimate where thunderstorm and lightning
> risk may develop over the next 30--180 minutes and converts that
> prediction into an explainable map and disaster-management alert.**

In simple words:

**Many weather signals → one common grid → AI fusion → future risk → map
→ alert → action.**

------------------------------------------------------------------------

# 4. What We Are Building

VajraNow is not intended to be only a weather dashboard.

It is designed as a **nowcasting + decision-support pipeline**.

The system has five major stages:

``` text
OBSERVE
   ↓
Collect atmospheric observations
   ↓
FUSE
   ↓
Align radar + satellite + lightning + atmospheric/model data
   ↓
PREDICT
   ↓
AI estimates thunderstorm / lightning risk
   ↓
EXPLAIN
   ↓
Show the signals contributing to the risk
   ↓
ALERT
   ↓
Support disaster-management action
```

This is the central architecture of the project.

------------------------------------------------------------------------

# 5. Why Multiple Sensors?

No single observation source tells the complete story.

## 5.1 Radar

Radar provides information about precipitation/storm structure and
intensity.

A simplified interpretation is:

``` text
Radar reflectivity ↑
        +
Strong organized cell
        ↓
Higher precipitation/storm intensity signal
```

Example prototype input:

``` text
Radar Reflectivity = 48 dBZ
```

The dashboard represents this as a storm-intensity signal.

### Limitation

Radar coverage is not uniform everywhere, and radar observations can
have gaps, outages or quality issues.

This is one reason VajraNow is designed for multi-source fusion instead
of radar-only prediction.

------------------------------------------------------------------------

# 6. Satellite

Meteorological satellites provide wide-area observations of cloud
systems.

For VajraNow, satellite-derived features can include information related
to:

-   cloud-top temperature,
-   cloud development,
-   cloud motion,
-   water vapour,
-   atmospheric structure,
-   cloud evolution over time.

INSAT-3DS is a dedicated meteorological satellite designed for
meteorological observation and disaster warning. MOSDAC describes
products including Cloud Motion Vector, Water Vapour Wind, Upper
Tropospheric Humidity, temperature/humidity profiles and other derived
parameters.

Source:

https://mosdac.gov.in/insat-3s-introduction

### Why satellite matters

Satellite coverage can provide information over areas where a radar
signal may not be available.

It also helps the model understand **cloud evolution**, not just the
storm intensity observed at one moment.

------------------------------------------------------------------------

# 7. Lightning

Lightning observations provide a direct signal of electrical activity
associated with convective storms.

A simplified interpretation is:

``` text
Lightning activity ↑
        ↓
Electrical activity increasing
        ↓
Potentially stronger convective development
```

Example prototype input:

``` text
Lightning Activity = 17 strikes/min
```

The final system can use time sequences of lightning observations to
learn:

-   lightning density,
-   lightning growth,
-   lightning jump-like behaviour,
-   spatial concentration,
-   movement of electrical activity.

### Important prototype limitation

The current prototype uses controlled/demo lightning values.

It must not be presented as having been trained or validated on
operational nationwide lightning-location data.

For a production implementation, the system would require an authorized,
reliable lightning observation feed.

------------------------------------------------------------------------

# 8. Atmospheric / Model Data

The atmosphere provides the physical environment in which thunderstorms
develop.

Potential features include:

-   CAPE
-   CIN
-   humidity
-   temperature
-   wind
-   wind shear
-   pressure
-   moisture convergence
-   model-derived instability indicators

Our prototype compresses this idea into an **Atmospheric Instability**
feature.

Example:

``` text
Atmospheric Instability = 81%
```

In the production system, this would be replaced by physically
meaningful variables and/or derived indices from authorized observations
and numerical weather prediction data.

------------------------------------------------------------------------

# 9. The Core Innovation: Multi-Sensor Fusion

The key idea is not simply:

``` text
Radar → AI
```

Instead:

``` text
Radar ───────────┐
Satellite ───────┤
Lightning ───────┤
Atmosphere/NWP ──┤
                 ↓
          Common Data Grid
                 ↓
          Temporal Alignment
                 ↓
           AI Fusion Model
                 ↓
       Spatiotemporal Forecast
                 ↓
       Risk + Explanation + Alert
```

This allows the system to combine complementary evidence.

For example:

``` text
Radar says:
storm intensity is increasing

Satellite says:
cloud is rapidly developing

Lightning says:
electrical activity is increasing

Atmosphere says:
environment is unstable

                ↓

VajraNow

                ↓

High short-term thunderstorm risk
```

------------------------------------------------------------------------

# 10. What We Have Implemented in the Current Prototype

The current dashboard shown in the attached screenshots already
demonstrates the main user workflow.

## 10.1 Forecast Control

The dashboard includes:

-   Storm Scenario selector
-   Forecast Horizon slider
-   Demo Mode

Example:

``` text
Storm Scenario:
Active Thunderstorm

Forecast Horizon:
+60 min
```

This allows the demo operator to move through different storm conditions
without waiting for a real storm event.

------------------------------------------------------------------------

# 11. Prototype Storm Scenarios

The prototype uses controlled scenarios so the complete pipeline can be
demonstrated reliably.

Example scenario set:

  Scenario                 Radar   Lightning   Cloud Development   Instability
  --------------------- -------- ----------- ------------------- -------------
  Low Activity            22 dBZ       2/min                 35%           38%
  Developing Storm        38 dBZ       6/min                 55%           72%
  Active Thunderstorm     48 dBZ      17/min                 72%           81%
  Severe Storm            62 dBZ      28/min                 91%           94%
  Decaying Storm          28 dBZ       3/min                 41%           48%

These values are **prototype/demo inputs**, not operational weather
observations.

------------------------------------------------------------------------

# 12. Current Atmospheric Situation Dashboard

The dashboard displays four main signals:

``` text
Radar Reflectivity
48 dBZ

Lightning Activity
17 / min

Cloud Development
72%

Atmospheric Instability
81%
```

This gives the operator a quick view of the atmospheric state before
looking at the prediction.

The purpose is important:

> The operator should not see only a mysterious "97% risk" number. The
> system should also show the evidence behind that estimate.

------------------------------------------------------------------------

# 13. AI Risk Assessment

The current prototype converts the input features into a thunderstorm
probability.

Example shown in the dashboard:

``` text
Thunderstorm Probability
97.4%

Risk Status
SEVERE

Lightning Risk
68%

Forecast Lead
+60 min
```

The exact values are generated from the controlled prototype scenario.

They are **not real-world accuracy measurements**.

This distinction is important when presenting the system to judges.

------------------------------------------------------------------------

# 14. Risk Classification

The prototype uses configurable demonstration thresholds:

``` text
Probability < 0.30
        ↓
LOW

0.30 – 0.49
        ↓
WATCH

0.50 – 0.69
        ↓
WARNING

≥ 0.70
        ↓
SEVERE
```

These are **prototype thresholds**.

They should not be described as official IMD operational thresholds.

In a production deployment, thresholds should be calibrated against
historical events, false alarms, misses, geographic risk, and
operational requirements.

------------------------------------------------------------------------

# 15. Risk Map

The dashboard contains an interactive map.

It visualizes:

-   geographic region,
-   synthetic storm cells,
-   risk intensity,
-   high-risk areas,
-   forecast lead time,
-   risk assessment.

The current prototype uses OpenStreetMap as the base map and controlled
synthetic storm-risk fields.

The production version can display real geospatial prediction grids.

The intended output is:

``` text
                FUTURE RISK MAP

       LOW       MODERATE       HIGH
        ↓            ↓            ↓

   🟢🟢🟢🟢       🟡🟡🟡       🔴🔴
   🟢🟢🟢🟢       🟡🟡🟡       🔴🔴
   🟢🟢🟢🟢       🟡🟡🟡       🔴🔴

                 ↓

       Disaster-management action
```

------------------------------------------------------------------------

# 16. Forecast Lead Time

VajraNow is designed to provide multiple future horizons:

``` text
+30 min
+60 min
+90 min
+120 min
+150 min
+180 min
```

The prototype dashboard shows an example evolution:

``` text
+30 min   → 98%
+60 min   → 97%
+90 min   → 77%
+120 min  → 32%
+150 min  → 4%
+180 min  → 2%
```

Again, these are controlled demonstration outputs.

The important concept is that VajraNow does not produce only one static
warning.

It represents the **expected evolution of risk with time**.

------------------------------------------------------------------------

# 17. Explainability: "Why Is VajraNow Alerting?"

One of the most important dashboard sections is the explanation layer.

Instead of:

``` text
ALERT!
```

the system should answer:

``` text
Why?

Radar:
strong precipitation/storm signal

Lightning:
electrical activity increasing

Cloud:
rapid cloud development

Atmosphere:
unstable environment

Therefore:
short-term thunderstorm risk is elevated.
```

This improves operator trust and makes the model output easier to audit.

------------------------------------------------------------------------

# 18. Forecast Method Comparison

The prototype also includes baseline comparison.

Current controlled synthetic demonstration:

  -------------------------------------------------------------------------
  Method          Role                             MAE                  CSI
  --------------- --------------- -------------------- --------------------
  Persistence     Baseline                    0.2222\*             0.0000\*

  Optical Flow    Storm-motion                0.0000\*             1.0000\*
                  baseline                             

  VajraNow AI     Multi-feature      Pending real-data    Pending real-data
  Fusion          ML prototype              evaluation           evaluation
  -------------------------------------------------------------------------

`*` These values are from the controlled synthetic demonstration.

They must **not** be presented as proof that VajraNow beats operational
nowcasting.

------------------------------------------------------------------------

# 19. Why We Need Baselines

A weather AI can produce a visually impressive forecast and still add
little value.

Therefore, the final research evaluation should compare VajraNow
against:

### Persistence

Assume the current storm field remains approximately where it is.

``` text
Current field
     ↓
Same field later
```

### Optical Flow / Advection

Estimate how the observed storm field is moving and advect it forward.

``` text
Current storm
      ↓
Estimate motion
      ↓
Move storm forward
```

### VajraNow

Use multiple observations and learned temporal relationships.

``` text
Radar
Satellite
Lightning
Atmosphere
     ↓
AI
     ↓
Future probability field
```

The final scientific question is:

> Does multi-source AI add measurable skill beyond simple persistence
> and motion-based extrapolation?

That is the question the real-data evaluation must answer.

------------------------------------------------------------------------

# 20. Final Target AI Architecture

The current prototype uses a lightweight ML model so that we can build
and demonstrate the end-to-end system quickly.

The final research/production architecture can use a spatiotemporal
neural network such as:

-   ConvLSTM
-   U-Net based temporal architecture
-   PredRNN
-   Earth observation transformer architecture
-   other validated spatiotemporal models

A conceptual architecture is:

``` text
TIME t-30      TIME t-15        TIME t
   │              │               │
   ├── Radar ─────┼── Radar ──────┤
   ├── Satellite ─┼── Satellite ──┤
   ├── Lightning ─┼── Lightning ──┤
   └── Atmosphere └── Atmosphere ─┘
                  │
                  ↓
        Spatial + Temporal Alignment
                  │
                  ↓
          Multi-Sensor Encoder
                  │
                  ↓
        Spatiotemporal AI Model
                  │
                  ├───────────────┐
                  ↓               ↓
        Thunderstorm Risk     Lightning Risk
                  │               │
                  └───────┬───────┘
                          ↓
                 Geospatial Forecast
                          │
             ┌────────────┼────────────┐
             ↓            ↓            ↓
          +30 min      +60 min      +90…180
             │            │            │
             └────────────┼────────────┘
                          ↓
                Explainable Alert Layer
                          ↓
                  Disaster Management
```

------------------------------------------------------------------------

# 21. Data Engineering Pipeline

The hardest part of a real system is not only the AI model.

The data must first be made consistent.

## Step 1: Ingest

Collect observations from:

``` text
Doppler Weather Radar
INSAT / meteorological satellite
Lightning detection network
AWS / weather observations
NWP/model fields
GIS layers
```

## Step 2: Quality Control

Remove or flag:

-   missing observations,
-   corrupted files,
-   invalid values,
-   sensor outages,
-   duplicated timestamps,
-   spatial registration errors.

## Step 3: Temporal Alignment

Different sensors may update at different times.

Convert them to a common time grid.

Example:

``` text
10:00
10:10
10:20
10:30
...
```

## Step 4: Spatial Alignment

Convert observations into a common geographic grid.

Example:

``` text
Latitude × Longitude × Time
```

## Step 5: Feature Engineering

Create model-ready features such as:

-   radar reflectivity,
-   radar motion,
-   cloud-top temperature,
-   cloud cooling rate,
-   cloud motion,
-   lightning density,
-   lightning trend,
-   CAPE,
-   CIN,
-   humidity,
-   wind,
-   wind shear.

## Step 6: AI Inference

Run the trained model.

## Step 7: Post-processing

Generate:

-   probability map,
-   risk category,
-   lightning risk,
-   forecast trajectory,
-   uncertainty,
-   explanation.

## Step 8: Alert Delivery

Send relevant alerts to the appropriate users.

------------------------------------------------------------------------

# 22. Final Real-Time Architecture

The target production architecture can be organized like this:

``` text
                    DATA SOURCES
                         │
       ┌─────────────────┼──────────────────┐
       │                 │                  │
     RADAR            SATELLITE         LIGHTNING
       │                 │                  │
       └─────────────────┼──────────────────┘
                         │
                  ATMOSPHERIC / NWP
                         │
                         ↓
                 DATA INGESTION
                         │
                         ↓
                QUALITY CONTROL
                         │
                         ↓
             TIME + SPACE ALIGNMENT
                         │
                         ↓
                  FEATURE STORE
                         │
                         ↓
                  AI NOWCASTER
                         │
              ┌──────────┴──────────┐
              ↓                     ↓
       THUNDERSTORM              LIGHTNING
          RISK                     RISK
              │                     │
              └──────────┬──────────┘
                         ↓
                  RISK ENGINE
                         │
                         ↓
              GIS / MAP VISUALIZATION
                         │
                         ↓
               EXPLANATION ENGINE
                         │
                         ↓
                 ALERT GATEWAY
                         │
       ┌─────────────────┼──────────────────┐
       ↓                 ↓                  ↓
 Control Room       Field Officers       Public
 Dashboard          / Responders       Notifications
```

------------------------------------------------------------------------

# 23. Disaster Management Workflow

VajraNow becomes useful when the prediction is connected to an action.

## Example: Thunderstorm Approaching a Rural District

Imagine a district containing:

-   villages,
-   farms,
-   schools,
-   construction sites,
-   roads,
-   power infrastructure.

At 3:00 PM, the system receives new observations.

### Observation

``` text
Radar:
strong cell forming

Satellite:
rapid cloud growth

Lightning:
electrical activity increasing

Atmosphere:
unstable

Storm motion:
toward the district
```

### VajraNow forecast

``` text
+30 min → HIGH
+60 min → SEVERE
+90 min → MODERATE
```

### Risk map

The high-risk area intersects several villages and an outdoor
agricultural area.

### Disaster-management action

The district control room can:

1.  Notify field officers.
2.  Issue a localized public warning.
3.  Advise people to move indoors.
4.  Stop outdoor government activities temporarily.
5.  Warn schools and event organizers.
6.  Coordinate with electricity and emergency teams.
7.  Monitor the storm through the next forecast cycle.

### New observations arrive

After 10--15 minutes, the system receives new data.

The forecast is updated.

If the storm weakens:

``` text
SEVERE → WARNING → WATCH
```

If it intensifies:

``` text
WARNING → SEVERE
```

This creates a continuous **observe → predict → act → observe again**
loop.

------------------------------------------------------------------------

# 24. Who Can Use VajraNow?

## 24.1 Disaster Management Authorities

Use the map to identify high-risk areas and prioritize field action.

## 24.2 District Control Rooms

Monitor changing storm risk across districts.

## 24.3 Emergency Response Teams

Use lead-time information to prepare personnel and equipment.

## 24.4 Agriculture Departments

Provide localized alerts to outdoor agricultural communities through
authorized channels.

## 24.5 Schools and Institutions

Use warnings to postpone outdoor activities when appropriate.

## 24.6 Power / Utility Operators

Prepare for possible storm-related disruptions.

## 24.7 Transport Authorities

Monitor hazardous weather along roads and transport corridors.

## 24.8 Public-Facing Systems

A simplified warning can eventually be distributed through:

-   mobile applications,
-   SMS,
-   web notifications,
-   public information systems,
-   authorized messaging channels.

The prototype is a decision-support demonstration, not an operational
public warning authority.

------------------------------------------------------------------------

# 25. Existing Solutions and the Gap

VajraNow should be presented as **complementary to existing
meteorological systems**, not as a replacement for them.

## 25.1 IMD Nowcast Warnings

IMD already provides district-wise and station-wise nowcast warnings
through its weather information infrastructure.

IMD pages also expose radar products and radar-based nowcast
information.

Examples:

-   IMD Nowcast Warning:\
    https://mausam.imd.gov.in/imd_latest/contents/stationwise-nowcast-warning_mc.php?id=1

-   IMD district-wise nowcast:\
    https://mausam.imd.gov.in/responsive/districtWiseNowcastGIS.php

-   IMD radar products:\
    https://mausam.imd.gov.in/hyderabad/radar/radarprd.html

### What this tells us

Operational weather services already have:

-   radar observations,
-   warnings,
-   district-level products,
-   specialized forecasts,
-   public dissemination channels.

Therefore our project should not claim that no existing weather warning
system exists.

------------------------------------------------------------------------

# 26. Damini Lightning App

IMD/MoES also identifies **Damini Lightning** as a dedicated lightning
alert application.

IMD pages list Damini alongside MAUSAM and other weather applications.

Source:

https://mausam.imd.gov.in/index_en.php

IMD's Vision 2047 document also describes Damini as a dedicated
lightning-alert application and identifies radar coverage and
thunderstorm detection as continuing challenge areas.

Source:

https://mausam.imd.gov.in/Forecast/mcmarq/mcmarq_data/IMD%20Vision_2047_10-01-2025.pdf

### Therefore

VajraNow should not claim:

> "There is no lightning alert system."

Instead, the correct statement is:

> **Existing systems already provide valuable warnings and lightning
> information. VajraNow proposes an AI-based multi-sensor fusion layer
> that can combine heterogeneous observations into a continuously
> updated, probabilistic, spatial-temporal decision-support product.**

------------------------------------------------------------------------

# 27. Satellite and MOSDAC Infrastructure

MOSDAC provides access to meteorological satellite data and products.

INSAT-3DS is specifically designed for meteorological observation and
disaster warning.

MOSDAC lists products including:

-   Cloud Motion Vector,
-   Water Vapour Wind,
-   Upper Tropospheric Humidity,
-   temperature/humidity profiles,
-   Outgoing Longwave Radiation,
-   Quantitative Precipitation Estimation,
-   and other derived products.

Sources:

https://mosdac.gov.in/insat-3s-introduction

https://www.mosdac.gov.in/insat-3dr-data-products

This supports the feasibility of using satellite observations as one
component of the multi-sensor pipeline.

------------------------------------------------------------------------

# 28. What Is Different About VajraNow?

The differentiation should be described as a **system-level
combination**, not as a claim that every individual component is new.

## Existing systems can provide

``` text
Radar information
Satellite information
Lightning alerts
Weather forecasts
District warnings
```

## VajraNow aims to combine these into

``` text
Multi-source observations
        ↓
Common spatial-temporal representation
        ↓
AI fusion
        ↓
30–180 minute probabilistic forecast
        ↓
Risk map
        ↓
Why-alert explanation
        ↓
Decision-support action
```

The important engineering focus is the **fusion + forecasting +
explanation + action workflow**.

------------------------------------------------------------------------

# 29. Why AI?

Traditional methods can be useful, especially for short lead times.

For example:

### Persistence

``` text
Assume current storm remains
```

Very simple and useful as a baseline.

### Motion extrapolation / optical flow

``` text
Observe movement
      ↓
Estimate motion
      ↓
Move storm forward
```

This can be effective when an existing storm cell is moving
consistently.

### Limitation

A purely motion-based method has difficulty with phenomena such as:

``` text
NEW STORM CELL FORMS
```

because a storm that does not exist yet has no observed shape to simply
move forward.

AI can potentially learn relationships associated with:

-   growth,
-   decay,
-   initiation,
-   interaction,
-   environmental instability,
-   multi-sensor signals.

That is why the final system is designed as a learned spatiotemporal
fusion system.

------------------------------------------------------------------------

# 30. Our Prototype AI

Because this is a hackathon prototype, we deliberately avoided heavy
model training at the first stage.

The current prototype uses a lightweight **Random Forest** model.

Conceptually:

``` text
Radar
Lightning
Cloud Development
Atmospheric Instability
        ↓
Random Forest
        ↓
Thunderstorm Probability
```

This allowed us to validate:

-   data flow,
-   feature handling,
-   model loading,
-   prediction,
-   risk classification,
-   dashboard integration,
-   map visualization,
-   forecast display.

The Random Forest should be treated as a **prototype AI component**, not
the final scientific model.

------------------------------------------------------------------------

# 31. Final Model Strategy

Once real datasets are available, the next stage is:

``` text
Historical sequences
        ↓
Multi-sensor alignment
        ↓
Training dataset
        ↓
Spatiotemporal model
        ↓
Validation
        ↓
Baseline comparison
        ↓
Calibration
        ↓
Deployment
```

A possible model design:

``` text
Radar sequence ──────┐
Satellite sequence ──┤
Lightning sequence ──┤
NWP sequence ────────┤
                      ↓
              Feature Encoders
                      ↓
          Spatiotemporal Fusion
                      ↓
                ConvLSTM/U-Net
                      ↓
              Probability Field
```

------------------------------------------------------------------------

# 32. Evaluation Plan

The final system should not be evaluated using only accuracy.

Weather events are spatially imbalanced: most grid cells may contain no
severe storm at a given moment.

Therefore, useful metrics include:

## MAE

Measures average error in continuous predictions.

## CSI

Critical Success Index.

Useful for event-based forecast verification.

## POD

Probability of Detection.

Measures how many observed events were correctly detected.

## FAR

False Alarm Ratio.

Measures the fraction of predicted events that did not occur.

## Precision / Recall

Useful for evaluating event detection.

## Brier Score

Useful for probabilistic forecasts.

## Lead-Time Skill

Measure performance separately at:

``` text
+30 min
+60 min
+90 min
+120 min
+150 min
+180 min
```

The final result should show how forecast skill changes as lead time
increases.

------------------------------------------------------------------------

# 33. What Success Looks Like

The final scientific target is not:

> "Our dashboard looks good."

It is:

> **VajraNow provides measurable additional skill over appropriate
> baselines while producing useful, explainable and actionable
> short-term risk information.**

A strong evaluation would show:

``` text
Baseline
    ↓
Forecast quality

Optical Flow
    ↓
Forecast quality

VajraNow
    ↓
Forecast quality
```

for multiple events and multiple lead times.

------------------------------------------------------------------------

# 34. Missing Data and Failure Handling

A real disaster-management system cannot assume every sensor is always
available.

## Radar unavailable

Use:

``` text
Satellite + Lightning + Atmosphere/NWP
```

## Lightning feed unavailable

Use:

``` text
Radar + Satellite + Atmosphere/NWP
```

and explicitly lower confidence.

## Satellite unavailable

Use:

``` text
Radar + Lightning + NWP
```

## Network interruption

Use the most recent valid data and clearly show data freshness.

## Model unavailable

Fall back to a simpler baseline or operational feed where authorized.

The system should never silently pretend that missing data is available.

------------------------------------------------------------------------

# 35. Confidence and Explainability

The final product should show more than probability.

A possible final panel:

``` text
THUNDERSTORM RISK
82%

LIGHTNING RISK
71%

FORECAST LEAD
+60 min

CONFIDENCE
Medium

MAIN CONTRIBUTORS
✓ Radar intensity increasing
✓ Cloud-top cooling/development
✓ Lightning activity increasing
✓ Atmospheric instability high

DATA QUALITY
Radar: Good
Satellite: Good
Lightning: Good
NWP: Good
```

This makes the output more useful for an operator.

------------------------------------------------------------------------

# 36. Disaster Management Alert Levels

The prototype can use simple risk categories:

``` text
LOW
No immediate action indicated.

WATCH
Monitor the area and prepare.

WARNING
Prepare field teams and communicate risk.

SEVERE
Immediate preparedness / escalation according to
authorized disaster-management procedures.
```

These descriptions are conceptual prototype language.

Operational alert categories must be defined and approved by the
responsible meteorological/disaster-management authority.

------------------------------------------------------------------------

# 37. Example End-to-End Scenario

## 14:00

The system receives a new observation cycle.

``` text
Radar:       moderate
Satellite:   cloud growth
Lightning:   increasing
Atmosphere:  unstable
```

VajraNow:

``` text
Risk = 42%
Status = WATCH
```

No major action yet, but the control room begins monitoring.

------------------------------------------------------------------------

## 14:20

New observations arrive.

``` text
Radar:       strong
Satellite:   rapid cloud development
Lightning:   strong increase
Atmosphere:  highly unstable
```

VajraNow:

``` text
Risk = 76%
Status = SEVERE
Lead = +60 min
```

The risk map shows that the storm trajectory is moving toward several
populated locations.

------------------------------------------------------------------------

## 14:25

The disaster-management operator sees:

``` text
WHY?

Radar              ↑
Cloud development  ↑
Lightning          ↑
Instability        ↑

Forecast:
High risk in next 30–60 minutes
```

The operator can initiate the appropriate authorized warning workflow.

------------------------------------------------------------------------

## 14:45

New data arrives.

The storm moves away from one area but intensifies toward another.

VajraNow updates the map.

``` text
Old risk zone
       ↓
Reduced

New risk zone
       ↓
Increased
```

This is the major operational idea:

> **The system continuously updates the location and timing of risk
> rather than treating a warning as a static message.**

------------------------------------------------------------------------

# 38. Current Prototype vs Final System

  ----------------------------------------------------------------------------
  Component               Current Prototype       Final Target
  ----------------------- ----------------------- ----------------------------
  Radar                   Controlled demo feature Real radar observations

  Satellite               Controlled              INSAT / authorized satellite
                          cloud-development       products
                          feature                 

  Lightning               Controlled demo feature Authorized
                                                  lightning-location
                                                  observations

  Atmosphere              Prototype instability   CAPE/CIN/humidity/wind/NWP
                          indicator               features

  AI                      Random Forest           Spatiotemporal AI

  Data                    Synthetic / controlled  Historical + near-real-time
                          demo                    data

  Forecast                30--180 min demo        Validated multi-lead
                                                  forecast

  Map                     Folium + OpenStreetMap  Production GIS/map layer

  Explainability          Feature evidence        Calibrated model
                                                  explanations

  Alerts                  Prototype UI            Authorized alert gateway

  Evaluation              Controlled synthetic    Real held-out events
                          demonstration           

  Deployment              Local Streamlit         Cloud/on-premise operational
                                                  service
  ----------------------------------------------------------------------------

------------------------------------------------------------------------

# 39. Technology Stack

## Prototype

``` text
Python
Streamlit
Scikit-learn
Pandas
NumPy
Folium
streamlit-folium
Joblib
```

## Future data/AI layer

Potential technologies:

``` text
PyTorch
Xarray
Rasterio
GeoPandas
Cartopy
PostGIS
Object storage
FastAPI
Redis / message queue
Docker
Kubernetes
```

The final stack should be selected according to actual data volume,
deployment requirements and institutional infrastructure.

------------------------------------------------------------------------

# 40. Current Repository Concept

Recommended project structure:

``` text
VajraNow/
│
├── app/
│   └── app.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│   └── vajranow_rf.pkl
│
├── notebooks/
│
├── src/
│   ├── ai_model.py
│   ├── preprocessing.py
│   ├── forecasting.py
│   └── visualization.py
│
├── requirements.txt
├── test.py
└── README.md
```

------------------------------------------------------------------------

# 41. Dashboard Sections

The current dashboard contains the following conceptual sections:

### 1. VajraNow header

``` text
VajraNow
Real-Time AI-Based Thunderstorm & Lightning Nowcasting
AI ENGINE ONLINE
```

### 2. Forecast Control

``` text
Storm Scenario
Forecast Horizon
Demo Mode
```

### 3. Current Atmospheric Situation

``` text
Radar
Lightning
Cloud
Instability
```

### 4. Alert

``` text
Risk status
Forecast lead
Preparedness message
```

### 5. Risk Map

``` text
Storm cells
Risk field
Geographic context
```

### 6. Risk Assessment

``` text
Thunderstorm Probability
Lightning Risk
Forecast Lead
Status
```

### 7. Why VajraNow Is Alerting

``` text
Radar
Lightning
Cloud Growth
Instability
```

### 8. Storm Risk Evolution

``` text
+30
+60
+90
+120
+150
+180
```

### 9. Forecast Probability Curve

Shows risk evolution over the forecast horizon.

### 10. Forecast Method Comparison

Compares baseline methods with the VajraNow AI prototype.

### 11. How VajraNow Works

``` text
Radar
Satellite
Lightning
Atmosphere
        ↓
AI Fusion
```

------------------------------------------------------------------------

# 42. Prototype Screenshots

The supplied prototype screenshots are included in:

``` text
docs/screenshots/
```

### Dashboard

![VajraNow Dashboard](docs/screenshots/05_dashboard_top.png)

### Risk Map

![VajraNow Risk Map](docs/screenshots/04_risk_map_and_assessment.png)

### Explainability and Forecast Evolution

![Explainability](docs/screenshots/03_explainability_and_risk_evolution.png)

### Forecast Comparison

![Forecast
Comparison](docs/screenshots/02_forecast_probability_and_comparison.png)

### How VajraNow Works

![Architecture UI](docs/screenshots/01_how_vajranow_works.png)

------------------------------------------------------------------------

# 43. Important Prototype Disclaimer

The current dashboard is a **proof-of-concept**.

The following numbers shown in the UI are controlled/demo outputs:

``` text
97.4% probability
68% lightning risk
48 dBZ
17 lightning/min
72% cloud development
81% instability
```

They are not evidence of operational forecast accuracy.

Similarly, the current baseline values are from a controlled synthetic
demonstration.

Before claiming real-world performance, the system must be evaluated
using:

-   real historical observations,
-   properly aligned multi-source datasets,
-   held-out storm events,
-   independent test periods,
-   appropriate meteorological metrics,
-   calibrated probabilities,
-   baseline comparisons.

This honesty is part of the engineering design.

------------------------------------------------------------------------

# 44. What We Should Say to Judges

## 30-second explanation

> "Our problem is short-term thunderstorm and lightning nowcasting.
> Existing weather systems provide radar, satellite, lightning and
> warning products, but the SIH problem asks us to build an AI/ML-based
> nowcasting solution using multiple atmospheric observations. VajraNow
> creates a common spatial-temporal representation of radar, satellite,
> lightning and atmospheric data, uses AI to estimate thunderstorm and
> lightning risk for the next 30 to 180 minutes, and presents the result
> as an explainable risk map with lead time and actionable decision
> support. Our current prototype validates the complete workflow with
> controlled inputs, while the final system is designed for real-data
> training and validation."

------------------------------------------------------------------------

# 45. If a Judge Asks: "Isn't This Already Available?"

Answer:

> "Yes, existing systems such as IMD's nowcast services, radar products,
> MAUSAM and Damini already provide important operational weather and
> lightning information. We are not claiming to replace them. Our
> contribution is a proposed AI fusion layer that combines heterogeneous
> observations into a continuously updated probabilistic spatial
> forecast, explains the signals contributing to the risk, and connects
> that forecast to a disaster-management workflow. The final claim will
> be supported by real-data evaluation against persistence and
> motion-based baselines."

This is a much stronger answer than saying existing systems do not
exist.

------------------------------------------------------------------------

# 46. If a Judge Asks: "Why AI?"

Answer:

> "Because a thunderstorm is a spatiotemporal process. Its movement is
> important, but so are initiation, growth, decay and environmental
> conditions. A learned model can combine multiple observation sequences
> and learn relationships that are difficult to represent with a single
> motion-extrapolation rule. We still compare against persistence and
> optical-flow baselines because AI must demonstrate measurable added
> value."

------------------------------------------------------------------------

# 47. If a Judge Asks: "Why Not Just Radar?"

Answer:

> "Radar is extremely valuable, but a single sensor does not describe
> the complete atmospheric state and radar coverage is not uniform.
> Satellite provides wider cloud information, lightning provides
> electrical activity, and atmospheric/model variables describe the
> environment. Multi-sensor fusion provides complementary evidence and
> also gives the system a path to degrade gracefully when one source is
> unavailable."

------------------------------------------------------------------------

# 48. If a Judge Asks: "What Is Actually Implemented?"

Answer honestly:

> "We have implemented the end-to-end prototype dashboard,
> scenario-based data generation, Random Forest inference, risk
> classification, forecast horizons, interactive risk visualization,
> explainability cards, storm-risk evolution and baseline comparison.
> The current values are controlled demonstration inputs. Real-data
> ingestion, large-scale training and operational validation are the
> next implementation stage."

------------------------------------------------------------------------

# 49. If a Judge Asks: "Where Is the Real Data?"

Answer:

> "The current hackathon prototype uses controlled inputs so that the
> complete system can be demonstrated reliably. The architecture is
> modular: the demo data layer can be replaced by authorized radar,
> satellite, lightning and atmospheric feeds without redesigning the
> dashboard and prediction workflow. The production stage requires
> data-access agreements, historical archives, quality control and
> independent validation."

------------------------------------------------------------------------

# 50. If a Judge Asks: "How Will You Deploy It?"

Possible architecture:

``` text
             Real-Time Data Feeds
                     ↓
              Message / Queue
                     ↓
             Data Processing
                     ↓
               AI Inference
                     ↓
                GIS Server
                     ↓
              Web Dashboard
                     ↓
          Authorized Alert APIs
```

Deployment can be:

-   government/private cloud,
-   institutional data centre,
-   containerized service,
-   hybrid architecture.

The final choice depends on data-access and operational requirements.

------------------------------------------------------------------------

# 51. Disaster Management Value

The value of VajraNow is not the probability number by itself.

The value is the chain:

``` text
Earlier signal
      ↓
Earlier forecast
      ↓
Earlier awareness
      ↓
Earlier preparedness
      ↓
Faster coordinated response
```

The system can help answer:

``` text
WHERE?
↓
Risk map

WHEN?
↓
Lead time

HOW SEVERE?
↓
Probability / risk

WHY?
↓
Evidence

WHAT NEXT?
↓
Preparedness workflow
```

That is the decision-support value of the platform.

------------------------------------------------------------------------

# 52. Key Innovation Points

## 1. Multi-sensor fusion

Combines complementary atmospheric signals.

## 2. Spatiotemporal forecasting

Focuses on both location and time.

## 3. Multi-lead forecast

Provides a sequence of future horizons instead of one static value.

## 4. Explainable risk

Shows the main signals contributing to an alert.

## 5. Radar-gap resilience

Can use other observations when one data source is unavailable, subject
to data quality.

## 6. Decision-support workflow

Connects prediction to disaster-management action.

## 7. Baseline-aware evaluation

Measures the AI against persistence and motion-based methods.

------------------------------------------------------------------------

# 53. What Makes the Approach Strong

The strength of VajraNow is the **end-to-end design**.

Many weather components can exist independently:

``` text
Radar
Satellite
Lightning
Forecast
Map
Alert
```

VajraNow organizes them into one pipeline:

``` text
OBSERVE
    ↓
FUSE
    ↓
PREDICT
    ↓
EXPLAIN
    ↓
ACT
    ↓
UPDATE
```

The final system should be judged by measurable forecast skill and
operational usefulness, not by the number of dashboard features.

------------------------------------------------------------------------

# 54. What Is Still Left for the Final Production Version?

## Phase 1: Prototype

Completed/implemented:

-   [x] Dashboard
-   [x] Scenario selection
-   [x] Forecast horizon
-   [x] Demo mode
-   [x] Prototype AI
-   [x] Risk classification
-   [x] Interactive map
-   [x] Risk assessment
-   [x] Explainability
-   [x] Forecast evolution
-   [x] Baseline comparison
-   [x] Architecture presentation

## Phase 2: Real-data research prototype

Next:

-   [ ] Acquire authorized historical datasets
-   [ ] Build data ingestion modules
-   [ ] Radar preprocessing
-   [ ] Satellite preprocessing
-   [ ] Lightning preprocessing
-   [ ] NWP/atmospheric preprocessing
-   [ ] Time synchronization
-   [ ] Geographic regridding
-   [ ] Missing-data handling
-   [ ] Build sequence dataset
-   [ ] Train spatiotemporal model
-   [ ] Compare against persistence
-   [ ] Compare against optical flow
-   [ ] Calculate POD/FAR/CSI/MAE/Brier score
-   [ ] Calibrate probabilities

## Phase 3: Operational architecture

-   [ ] Real-time ingestion
-   [ ] Model serving
-   [ ] Monitoring
-   [ ] Data-quality monitoring
-   [ ] GIS backend
-   [ ] Alert gateway
-   [ ] Authentication and authorization
-   [ ] Audit logs
-   [ ] Failover
-   [ ] Load testing
-   [ ] Security review
-   [ ] Operational validation with domain experts

------------------------------------------------------------------------

# 55. Recommended Final Demo Story

For a 3-minute SIH video:

``` text
0:00 – 0:20
THE PROBLEM

Show real thunderstorm/lightning imagery.

Voice:
“Thunderstorms can intensify and move rapidly. The challenge is not only detecting a storm, but knowing where the risk will be in the next few minutes.”

0:20 – 0:45
THE DATA

Show radar + satellite + lightning visuals.

Voice:
“VajraNow combines multiple atmospheric observations instead of depending on a single signal.”

0:45 – 1:05
THE ARCHITECTURE

Show:

Radar
Satellite
Lightning
Atmosphere
      ↓
AI Fusion
      ↓
Risk Forecast
      ↓
Alert

1:05 – 2:20
LIVE DEMO

Show:

Scenario
↓
Atmospheric values
↓
Risk map
↓
+60 min forecast
↓
Why alert?
↓
Risk evolution

2:20 – 2:40
VALIDATION

Show:

Persistence
Optical Flow
VajraNow

Explain that current demo values are controlled and real-data evaluation is the next stage.

2:40 – 3:00
DISASTER MANAGEMENT

Show:

High-risk region
↓
Control room
↓
Field response
↓
Public preparedness

End:

VajraNow

OBSERVE → FUSE → PREDICT → EXPLAIN → ALERT
```

------------------------------------------------------------------------

# 56. One Strong Final Pitch

> **"VajraNow is an AI-powered thunderstorm and lightning nowcasting
> platform designed for disaster-management decision support. It fuses
> radar, satellite, lightning and atmospheric observations into a common
> spatial-temporal representation, predicts short-term risk over
> multiple future horizons, explains why the risk is increasing, and
> visualizes where action may be required. Our prototype demonstrates
> this complete workflow with controlled inputs and a lightweight ML
> model. The next stage is real-data training and rigorous validation
> against persistence and optical-flow baselines, followed by real-time
> deployment and authorized alert integration."**

------------------------------------------------------------------------

# 57. Final Architecture Summary

``` text
                         VAJRANOW
                            │
                    Real-Time Nowcasting
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
      RADAR              SATELLITE          LIGHTNING
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                     ATMOSPHERE / NWP
                            │
                            ↓
                   DATA PREPROCESSING
                            │
                   TIME / SPACE ALIGNMENT
                            │
                            ↓
                    MULTI-SENSOR FUSION
                            │
                            ↓
                    SPATIOTEMPORAL AI
                            │
             ┌──────────────┴──────────────┐
             ↓                             ↓
      THUNDERSTORM RISK               LIGHTNING RISK
             │                             │
             └──────────────┬──────────────┘
                            ↓
                     FORECAST MAP
                            │
               +30 +60 +90 +120 +150 +180
                            │
                            ↓
                     EXPLAINABILITY
                            │
                            ↓
                   DECISION SUPPORT
                            │
             ┌──────────────┼──────────────┐
             ↓              ↓              ↓
        Control Room     Field Teams      Public
```

------------------------------------------------------------------------

# 58. Final Takeaway

VajraNow is best understood as a **forecast-to-action pipeline**.

It starts with observations:

``` text
RADAR
SATELLITE
LIGHTNING
ATMOSPHERE
```

It transforms them:

``` text
ALIGN → FUSE → LEARN → PREDICT
```

It communicates them:

``` text
MAP → PROBABILITY → EXPLANATION → ALERT
```

And it supports disaster management:

``` text
AWARENESS → PREPAREDNESS → RESPONSE
```

The current prototype proves that this complete interaction can be
demonstrated in one dashboard.

The final research/production version must prove that the AI adds
measurable skill on real, independent weather events and must be
integrated with authorized operational data and warning procedures.

------------------------------------------------------------------------

# 59. References

## Smart India Hackathon Problem Statement

SIH26072:

https://sih2026.vuce.in/ps/SIH26072

## India Meteorological Department

IMD main weather portal:

https://mausam.imd.gov.in/index_en.php

IMD district/station nowcast:

https://mausam.imd.gov.in/responsive/districtWiseNowcastGIS.php

IMD radar products:

https://mausam.imd.gov.in/hyderabad/radar/radarprd.html

IMD radar-based nowcast:

https://rmcnewdelhi.imd.gov.in/rwfc/nowcast/nowcast.php

## MOSDAC / ISRO

INSAT-3DS:

https://mosdac.gov.in/insat-3s-introduction

INSAT-3DR products:

https://www.mosdac.gov.in/insat-3dr-data-products

## Lightning

IMD / MoES references to Damini Lightning:

https://mausam.imd.gov.in/index_en.php

------------------------------------------------------------------------

# 60. Final Note

**VajraNow is a prototype and research-oriented demonstration.**

It should not be presented as an operational replacement for IMD
warnings, as a certified emergency-warning system, or as having
real-world forecast accuracy until the real-data validation and
operational approval stages are completed.

The goal of the project is to demonstrate a technically defensible path
from:

> **multi-source atmospheric observations → AI nowcasting → explainable
> risk → disaster-management decision support.**

**⚡ VajraNow: Observe → Fuse → Predict → Explain → Alert**
