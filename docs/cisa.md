# CISA Decision Model

CISA Stakeholder-Specific Vulnerability Categorization

**Version:** 1.0  
**Reference:** [https://www.cisa.gov/stakeholder-specific-vulnerability-categorization-ssvc](https://www.cisa.gov/stakeholder-specific-vulnerability-categorization-ssvc)

## Decision Tree

```mermaid
flowchart LR
    ExploitationStatus_1{ExploitationStatus}
    AutomatableStatus_2{AutomatableStatus}
    ExploitationStatus_1 -->|NONE| AutomatableStatus_2
    TechnicalImpactLevel_3{TechnicalImpactLevel}
    AutomatableStatus_2 -->|YES| TechnicalImpactLevel_3
    MissionWellbeingImpactLevel_4{MissionWellbeingImpactLevel}
    TechnicalImpactLevel_3 -->|TOTAL| MissionWellbeingImpactLevel_4
    Action_ATTEND_5[ATTEND]
    MissionWellbeingImpactLevel_4 -->|HIGH| Action_ATTEND_5
    TechnicalImpactLevel_6{TechnicalImpactLevel}
    AutomatableStatus_2 -->|NO| TechnicalImpactLevel_6
    MissionWellbeingImpactLevel_7{MissionWellbeingImpactLevel}
    TechnicalImpactLevel_6 -->|TOTAL| MissionWellbeingImpactLevel_7
    Action_TRACK_STAR_8[TRACK_STAR]
    MissionWellbeingImpactLevel_7 -->|HIGH| Action_TRACK_STAR_8
    AutomatableStatus_9{AutomatableStatus}
    ExploitationStatus_1 -->|POC| AutomatableStatus_9
    TechnicalImpactLevel_10{TechnicalImpactLevel}
    AutomatableStatus_9 -->|YES| TechnicalImpactLevel_10
    MissionWellbeingImpactLevel_11{MissionWellbeingImpactLevel}
    TechnicalImpactLevel_10 -->|TOTAL| MissionWellbeingImpactLevel_11
    Action_TRACK_STAR_12[TRACK_STAR]
    MissionWellbeingImpactLevel_11 -->|MEDIUM| Action_TRACK_STAR_12
    Action_ATTEND_13[ATTEND]
    MissionWellbeingImpactLevel_11 -->|HIGH| Action_ATTEND_13
    MissionWellbeingImpactLevel_14{MissionWellbeingImpactLevel}
    TechnicalImpactLevel_10 -->|PARTIAL| MissionWellbeingImpactLevel_14
    Action_ATTEND_15[ATTEND]
    MissionWellbeingImpactLevel_14 -->|HIGH| Action_ATTEND_15
    TechnicalImpactLevel_16{TechnicalImpactLevel}
    AutomatableStatus_9 -->|NO| TechnicalImpactLevel_16
    MissionWellbeingImpactLevel_17{MissionWellbeingImpactLevel}
    TechnicalImpactLevel_16 -->|PARTIAL| MissionWellbeingImpactLevel_17
    Action_TRACK_STAR_18[TRACK_STAR]
    MissionWellbeingImpactLevel_17 -->|HIGH| Action_TRACK_STAR_18
    MissionWellbeingImpactLevel_19{MissionWellbeingImpactLevel}
    TechnicalImpactLevel_16 -->|TOTAL| MissionWellbeingImpactLevel_19
    Action_TRACK_STAR_20[TRACK_STAR]
    MissionWellbeingImpactLevel_19 -->|MEDIUM| Action_TRACK_STAR_20
    Action_ATTEND_21[ATTEND]
    MissionWellbeingImpactLevel_19 -->|HIGH| Action_ATTEND_21
    AutomatableStatus_22{AutomatableStatus}
    ExploitationStatus_1 -->|ACTIVE| AutomatableStatus_22
    TechnicalImpactLevel_23{TechnicalImpactLevel}
    AutomatableStatus_22 -->|YES| TechnicalImpactLevel_23
    MissionWellbeingImpactLevel_24{MissionWellbeingImpactLevel}
    TechnicalImpactLevel_23 -->|PARTIAL| MissionWellbeingImpactLevel_24
    Action_ATTEND_25[ATTEND]
    MissionWellbeingImpactLevel_24 -->|LOW| Action_ATTEND_25
    Action_ATTEND_26[ATTEND]
    MissionWellbeingImpactLevel_24 -->|MEDIUM| Action_ATTEND_26
    Action_ACT_27[ACT]
    MissionWellbeingImpactLevel_24 -->|HIGH| Action_ACT_27
    MissionWellbeingImpactLevel_28{MissionWellbeingImpactLevel}
    TechnicalImpactLevel_23 -->|TOTAL| MissionWellbeingImpactLevel_28
    Action_ATTEND_29[ATTEND]
    MissionWellbeingImpactLevel_28 -->|LOW| Action_ATTEND_29
    Action_ACT_30[ACT]
    MissionWellbeingImpactLevel_28 -->|MEDIUM| Action_ACT_30
    Action_ACT_31[ACT]
    MissionWellbeingImpactLevel_28 -->|HIGH| Action_ACT_31
    TechnicalImpactLevel_32{TechnicalImpactLevel}
    AutomatableStatus_22 -->|NO| TechnicalImpactLevel_32
    MissionWellbeingImpactLevel_33{MissionWellbeingImpactLevel}
    TechnicalImpactLevel_32 -->|PARTIAL| MissionWellbeingImpactLevel_33
    Action_ATTEND_34[ATTEND]
    MissionWellbeingImpactLevel_33 -->|HIGH| Action_ATTEND_34
    MissionWellbeingImpactLevel_35{MissionWellbeingImpactLevel}
    TechnicalImpactLevel_32 -->|TOTAL| MissionWellbeingImpactLevel_35
    Action_ATTEND_36[ATTEND]
    MissionWellbeingImpactLevel_35 -->|MEDIUM| Action_ATTEND_36
    Action_ACT_37[ACT]
    MissionWellbeingImpactLevel_35 -->|HIGH| Action_ACT_37
```

## Decision Points

- **ExploitationStatus**: `NONE`, `POC`, `ACTIVE`
- **AutomatableStatus**: `YES`, `NO`
- **TechnicalImpactLevel**: `PARTIAL`, `TOTAL`
- **MissionWellbeingImpactLevel**: `LOW`, `MEDIUM`, `HIGH`

## Usage

```python
from ssvc.plugins.cisa import DecisionCisa

decision = DecisionCisa(
    # Set decision point values here
)

outcome = decision.evaluate()
print(f"Action: {outcome.action}")
print(f"Priority: {outcome.priority}")
```