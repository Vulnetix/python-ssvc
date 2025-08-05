# Coordinator Publication Decision Model Decision Model

CERT/CC Coordinator Publication Decision Model for determining vulnerability disclosure

**Version:** 1.0  
**Reference:** [https://certcc.github.io/SSVC/howto/publication_decision/](https://certcc.github.io/SSVC/howto/publication_decision/)

## Decision Tree

```mermaid
flowchart LR
    SupplierInvolvement_1{SupplierInvolvement}
    ExploitationStatus_2{ExploitationStatus}
    SupplierInvolvement_1 -->|FIX_READY| ExploitationStatus_2
    PublicValueAdded_3{PublicValueAdded}
    ExploitationStatus_2 -->|NONE| PublicValueAdded_3
    Action_DO_NOT_PUBLISH_4[DO_NOT_PUBLISH]
    PublicValueAdded_3 -->|LIMITED| Action_DO_NOT_PUBLISH_4
    Action_DO_NOT_PUBLISH_5[DO_NOT_PUBLISH]
    PublicValueAdded_3 -->|AMPLIATIVE| Action_DO_NOT_PUBLISH_5
    Action_PUBLISH_6[PUBLISH]
    PublicValueAdded_3 -->|PRECEDENCE| Action_PUBLISH_6
    PublicValueAdded_7{PublicValueAdded}
    ExploitationStatus_2 -->|PUBLIC_POC| PublicValueAdded_7
    Action_DO_NOT_PUBLISH_8[DO_NOT_PUBLISH]
    PublicValueAdded_7 -->|LIMITED| Action_DO_NOT_PUBLISH_8
    Action_PUBLISH_9[PUBLISH]
    PublicValueAdded_7 -->|AMPLIATIVE| Action_PUBLISH_9
    Action_PUBLISH_10[PUBLISH]
    PublicValueAdded_7 -->|PRECEDENCE| Action_PUBLISH_10
    PublicValueAdded_11{PublicValueAdded}
    ExploitationStatus_2 -->|ACTIVE| PublicValueAdded_11
    Action_PUBLISH_12[PUBLISH]
    PublicValueAdded_11 -->|LIMITED| Action_PUBLISH_12
    Action_PUBLISH_13[PUBLISH]
    PublicValueAdded_11 -->|AMPLIATIVE| Action_PUBLISH_13
    Action_PUBLISH_14[PUBLISH]
    PublicValueAdded_11 -->|PRECEDENCE| Action_PUBLISH_14
    ExploitationStatus_15{ExploitationStatus}
    SupplierInvolvement_1 -->|COOPERATIVE| ExploitationStatus_15
    PublicValueAdded_16{PublicValueAdded}
    ExploitationStatus_15 -->|NONE| PublicValueAdded_16
    Action_DO_NOT_PUBLISH_17[DO_NOT_PUBLISH]
    PublicValueAdded_16 -->|LIMITED| Action_DO_NOT_PUBLISH_17
    Action_DO_NOT_PUBLISH_18[DO_NOT_PUBLISH]
    PublicValueAdded_16 -->|AMPLIATIVE| Action_DO_NOT_PUBLISH_18
    Action_PUBLISH_19[PUBLISH]
    PublicValueAdded_16 -->|PRECEDENCE| Action_PUBLISH_19
    PublicValueAdded_20{PublicValueAdded}
    ExploitationStatus_15 -->|PUBLIC_POC| PublicValueAdded_20
    Action_DO_NOT_PUBLISH_21[DO_NOT_PUBLISH]
    PublicValueAdded_20 -->|LIMITED| Action_DO_NOT_PUBLISH_21
    Action_PUBLISH_22[PUBLISH]
    PublicValueAdded_20 -->|AMPLIATIVE| Action_PUBLISH_22
    Action_PUBLISH_23[PUBLISH]
    PublicValueAdded_20 -->|PRECEDENCE| Action_PUBLISH_23
    PublicValueAdded_24{PublicValueAdded}
    ExploitationStatus_15 -->|ACTIVE| PublicValueAdded_24
    Action_PUBLISH_25[PUBLISH]
    PublicValueAdded_24 -->|LIMITED| Action_PUBLISH_25
    Action_PUBLISH_26[PUBLISH]
    PublicValueAdded_24 -->|AMPLIATIVE| Action_PUBLISH_26
    Action_PUBLISH_27[PUBLISH]
    PublicValueAdded_24 -->|PRECEDENCE| Action_PUBLISH_27
    ExploitationStatus_28{ExploitationStatus}
    SupplierInvolvement_1 -->|UNCOOPERATIVE_UNRESPONSIVE| ExploitationStatus_28
    PublicValueAdded_29{PublicValueAdded}
    ExploitationStatus_28 -->|NONE| PublicValueAdded_29
    Action_PUBLISH_30[PUBLISH]
    PublicValueAdded_29 -->|LIMITED| Action_PUBLISH_30
    Action_PUBLISH_31[PUBLISH]
    PublicValueAdded_29 -->|AMPLIATIVE| Action_PUBLISH_31
    Action_PUBLISH_32[PUBLISH]
    PublicValueAdded_29 -->|PRECEDENCE| Action_PUBLISH_32
    PublicValueAdded_33{PublicValueAdded}
    ExploitationStatus_28 -->|PUBLIC_POC| PublicValueAdded_33
    Action_PUBLISH_34[PUBLISH]
    PublicValueAdded_33 -->|LIMITED| Action_PUBLISH_34
    Action_PUBLISH_35[PUBLISH]
    PublicValueAdded_33 -->|AMPLIATIVE| Action_PUBLISH_35
    Action_PUBLISH_36[PUBLISH]
    PublicValueAdded_33 -->|PRECEDENCE| Action_PUBLISH_36
    PublicValueAdded_37{PublicValueAdded}
    ExploitationStatus_28 -->|ACTIVE| PublicValueAdded_37
    Action_PUBLISH_38[PUBLISH]
    PublicValueAdded_37 -->|LIMITED| Action_PUBLISH_38
    Action_PUBLISH_39[PUBLISH]
    PublicValueAdded_37 -->|AMPLIATIVE| Action_PUBLISH_39
    Action_PUBLISH_40[PUBLISH]
    PublicValueAdded_37 -->|PRECEDENCE| Action_PUBLISH_40
```

## Decision Points

- **SupplierInvolvement**: `FIX_READY`, `COOPERATIVE`, `UNCOOPERATIVE_UNRESPONSIVE`
- **ExploitationStatus**: `NONE`, `PUBLIC_POC`, `ACTIVE`
- **PublicValueAdded**: `LIMITED`, `AMPLIATIVE`, `PRECEDENCE`

## Usage

```python
from ssvc.plugins.coordinator_publication import DecisionCoordinatorPublication

decision = DecisionCoordinatorPublication(
    # Set decision point values here
)

outcome = decision.evaluate()
print(f"Action: {outcome.action}")
print(f"Priority: {outcome.priority}")
```