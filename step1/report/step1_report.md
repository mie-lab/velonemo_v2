# Step 1 — LLM vs. human (v1) extraction

_`gemini-3.1-flash-lite` · K=3 · match: name/definition (lexical+semantic) · fields scored where GT annotated._

| paper | GT | LLM | match | new | recall | prec | supp | type | scale | feature | criteria |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| beecham2023 | 12 | 13 | 12 | 2 | 100% | 92% | 0.90 | 100% | 92% | 100% | 100% |
| hardinghaus2021 | 5 | 5 | 3 | 0 | 60% | 60% | 0.80 | 67% | 100% | 100% | 100% |
| hsu2023 | 20 | 23 | 20 | 0 | 100% | 87% | 0.99 | 95% | 64% | — | 100% |
| krenn2015 | 6 | 5 | 5 | 0 | 83% | 100% | 1.00 | 80% | 80% | 100% | 100% |
| schmidquerg2021 | 4 | 4 | 4 | 0 | 100% | 100% | 1.00 | 100% | 0% | 0% | 100% |
| weikl2023 | 21 | 19 | 19 | 3 | 90% | 100% | 0.91 | 100% | 84% | 95% | 100% |
| santos2022 | 4 | 4 | 3 | 0 | 75% | 75% | 1.00 | 100% | 100% | 67% | 0% |
| ito2021 | 33 | 34 | 32 | 0 | 97% | 94% | 0.98 | 94% | 92% | 100% | 100% |
| abad2018 | 5 | 7 | 4 | 0 | 80% | 57% | 1.00 | 100% | 75% | 0% | 100% |
| daraei2021 | 7 | 7 | 7 | 1 | 100% | 100% | 1.00 | 100% | 100% | 86% | 100% |
| boisjoly2019 | 2 | 3 | 2 | 3 | 100% | 67% | 0.78 | 100% | 100% | 100% | 50% |
| reggiani2021 | 2 | 5 | 2 | 0 | 100% | 40% | 0.80 | 100% | 100% | 100% | 100% |
| soltani2022 | 5 | 6 | 4 | 1 | 80% | 67% | 0.83 | 100% | — | 75% | 0% |
| karolemeas2022 | 10 | 10 | 9 | 0 | 90% | 90% | 1.00 | 89% | 88% | 100% | 100% |
| codina2022 | 8 | 7 | 6 | 0 | 75% | 86% | 0.95 | 83% | 100% | 100% | 100% |
| **mean** | | | | | **89%** | **81%** | **0.93** | 94% | 84% | 80% | 83% |

_Extended fields (agreement where the human annotated it): unit 48% (n=14) · aggregate 42% (n=6) · scoring 13% (n=8) · buffer 66% (n=4) · parts 56% (n=3)._

### Legend
**Table columns**
- **paper** — the source paper (short key).
- **GT** — number of metrics the human annotated for this paper (the ground truth).
- **LLM** — number of metrics the model extracted.
- **match** — model metrics paired to a human one (same metric).
- **new** — metrics the model coined as NOT already in the ontology (`is_new`).
- **recall** — of the human's metrics, the share the model also found (match ÷ GT).
- **prec** — precision: of the model's metrics, the share that matched a human one (match ÷ LLM).
- **supp** — K-run stability: mean `support` over the paper's extracted metrics (1.00 = all K samples agreed on every metric; 0.67 = on average 2 of 3). Low supp = the extraction itself is unstable for this paper — read its scores with that uncertainty in mind.
- **type · scale · feature · criteria** — field agreement over matched pairs, model vs. human GT, scored ONLY where the human annotated that field: thematic **type** (of 6) · measurement **scale** (of 4) · representation **feature** (of 7) · **criteria** (goals, direct∪indirect — counts as agree if the sets overlap).
- _Extended fields line (above): the same field-agreement idea for the sparse fields unit · aggregate · scoring · buffer · parts._

**Per-pair marks** (in each paper's *Matched* list, e.g. `[T= S≠ F= C=]`)
- `[T S F C]` = agreement on **T**hematic type · measurement **S**cale · representation **F**eature · **C**riteria.
- `=` agree · `≠` differ · `·` the human left that field blank (so it is not scored).
- `⟵ …` lists the actual differing values (model ≠ human) — this is where a low / 0% score comes from.
- `⚠` flags a pair whose **GT-row type disagrees with the ontology** — a data inconsistency, not a model error.
## beecham2023 · _Connected Bikeability_

**Matched:**
- `IntersectionDensity` → `IntersectionDensity`  [T= S= F= C=]
- `SpeedLimit` → `MotorisedTrafficSpeed`  [T= S= F= C=]
- `OffRoadBikeLaneAndRouteShare` → `OffRoadBikeLaneAndRouteShare`  [T= S= F= C=]
- `SegregatedBikeLaneShare` → `SegregatedBikeLaneShare`  [T= S= F= C=]
- `PartSegregatedBikeLaneShare` → `PartSegregatedBikeLaneShare`  [T= S= F= C=]
- `AdvisoryAndMandatoryBikeLaneShare` → `AdvisoryAndMandatoryBikeLaneShare`  [T= S= F= C=]
- `SafetySupportedIntersectionShare` → `SafetySupportedIntersectionShare`  [T= S= F= C=]
- `GreenSpaceShare` → `GreenSpaceShare`  [T= S= F= C=]
- `BikeParkingDensity` → `BikeParkingDensity`  [T= S= F= C=]
- `DetourFactor` → `Sinuosity`  [T= S= F= C=]
- `SignageRatio` → `SignageRatio`  [T= S≠ F= C=]  ⟵ scale: ratio ≠ nominal
- `RightTurnVolume` → `RightTurnDensity`  [T= S= F= C=]
**Extra:** `RouteDistanceCoefficient`
**Newly minted:** `RightTurnVolume`, `RouteDistanceCoefficient`

## hardinghaus2021 · _Multifactorial Index of Urban Bikeability_

**Matched:**
- `IntersectionDensity` → `IntersectionDensity`  [T= S= F= C=]
- `GreenSpaceShare` → `GreenPathShare`  [T= S= F= C=]
- `BikeSharingStationDensity` → `BikeSharingAndServiceFacilityDensity`  [T≠ S= F= C=]  ⟵ type: InfrastructuralMetric ≠ CompositeMetric
**Missed:** `BikeLaneAlongMainStreetRatio`, `SlowStreetShare`
**Extra:** `RoadType`, `BikeLanePresence`

## hsu2023 · _Urban Bikeability Evaluation Framework_

**Matched:**
- `BikeLaneLength` → `BikeLaneWidth`  [T= S= F· C=]
- `BikeLaneWidth` → `BikeLaneType`  [T= S≠ F· C=]  ⟵ scale: ratio ≠ ordinal
- `SegregatedBikeLaneShare` → `BikeLaneSurfaceType`  [T= S≠ F· C=]  ⟵ scale: ratio ≠ nominal
- `BikeLaneSurfaceCondition` → `SidewalkSurfaceType`  [T= S≠ F· C=]  ⟵ scale: ordinal ≠ nominal
- `BikeParkingDensity` → `BikeParkingDensity`  [T= S= F· C=]
- `SidewalkWidth` → `SidewalkWidth`  [T= S= F· C=]
- `LightingPresence` → `DegreeOfGreenery`  [T≠ S· F· C=]  ⟵ type: InfrastructuralMetric ≠ ContextualMetric
- `BikeSharingStationDensity` → `BikeSharingStationDensity`  [T= S= F· C=]
- `DegreeOfGreenery` → `PerceivedAirQuality`  [T= S· F· C=]
- `TrafficVolume` → `MotorisedVehicleCount`  [T= S= F· C=]
- `BusTrafficFlow` → `BusAndCarTrafficVolumeRatio`  [T= S= F· C=]
- `PerceivedTrafficSpeed` → `PerceivedTrafficSpeed`  [T= S≠ F· C=]  ⟵ scale: ordinal ≠ ratio
- `PerceivedMixedTrafficConflict` → `PerceivedIntersectionMixedTrafficConflict`  [T= S· F· C=]
- `IllegalSideParkingDensity` → `IllegalSideParkingDensity`  [T= S= F· C=]
- `IntersectionDensity` → `IntersectionDensity`  [T= S= F· C=]
- `BikeLaneDensity` → `BikeLaneDensity`  [T= S= F· C=]
- `DegreeOfEnforcement` → `DegreeOfEnforcement`  [T= S· F· C=]
- `BicycleLawPromotion` → `BicycleLawPromotion`  [T= S· F· C=]
- `BicyclePolicyDissemination` → `BicyclePolicyDissemination`  [T= S· F· C=]
- `BicycleRidingEducation` → `BicycleRidingEducation`  [T= S≠ F· C=]  ⟵ scale: ordinal ≠ nominal
**Extra:** `PerceivedSidewalkSurfaceCondition`, `PerceivedAirQuality`, `LandUseMix`

## krenn2015 · _Bikeability Index (Krenn et al.)_

**Matched:**
- `BikeLaneDensity` → `BikeLaneDensity`  [T= S= F= C=]
- `SegregatedBikeLanePresence` → `SeparatedBikeLaneDensity`  [T≠ S≠ F= C=]  ⟵ type: InfrastructuralMetric ≠ MorphologicalMetric · scale: nominal ≠ ratio
- `MainRoadWithoutBikeLaneDensity` → `MainRoadWithoutBikeLaneDensity`  [T= S= F= C=]
- `GreenSpaceShare` → `GreenSpaceShare`  [T= S= F= C=]
- `Slope` → `Slope`  [T= S= F= C=]
**Missed:** `BikeLanePresence`

## schmidquerg2021 · _Munich Bikeability Index_

**Matched:**
- `BikeLaneType` → `BikeLaneType`  [T= S≠ F≠ C=]  ⟵ scale: ordinal ≠ nominal · feature: Edge ≠ GridCell
- `SpeedLimit` → `SpeedLimit`  [T= S≠ F≠ C=]  ⟵ scale: ordinal ≠ ratio · feature: Edge ≠ GridCell
- `BikeParkingType` → `BikeParkingType`  [T= S≠ F≠ C=]  ⟵ scale: ordinal ≠ nominal · feature: PointOfInterest ≠ GridCell
- `IntersectionType` → `IntersectionType`  [T= S≠ F≠ C=]  ⟵ scale: ordinal ≠ nominal · feature: Node ≠ GridCell

## weikl2023 · _Data-driven quality assessment of cycling networks_

**Matched:**
- `BikeLaneWidth` → `BikeLaneWidth`  [T= S= F= C=]
- `SpeedDifference` → `BikeAndCarSpeedDifference`  [T= S= F= C=]
- `CollisionRisk` → `BikeLaneTypeAndTrafficVolumeRatio`  [T= S≠ F= C=]  ⟵ scale: nominal ≠ ratio
- `DistanceToSideParking` → `DistanceToSideParking`  [T= S= F= C=]
- `ConflictPoints` → `IntersectionDensity`  [T= S= F= C=]
- `Illuminance` → `Illuminance`  [T= S= F= C=]
- `Slope` → `Slope`  [T= S≠ F= C=]  ⟵ scale: ratio ≠ ordinal
- `SurfaceTypeAndCondition` → `SurfaceTypeAndCondition`  [T= S= F= C=]
- `BrakingFrequency` → `BreakingFrequency`  [T= S= F= C=]
- `BikeParkingDensity` → `BikeParkingType`  [T= S≠ F≠ C=]  ⟵ scale: ratio ≠ nominal · feature: Route ≠ Node
- `DetourFactor` → `Sinuosity`  [T= S= F= C=]
- `TimeLossAtIntersection` → `TimeLossAtIntersection`  [T= S= F= C=]
- `BikeAndCarTravelTimeRatio` → `BikeAndCarTravelTimeRatio`  [T= S= F= C=]
- `BikeLaneDensity` → `BikeLaneDensity`  [T= S= F= C=]
- `OfficialBikeNetworkShare` → `OfficialBikeNetworkShare`  [T= S= F= C=]
- `SignagePresence` → `SignpostDensity`  [T= S= F= C=]
- `GreenSpaceShare` → `GreenSpaceShare`  [T= S= F= C=]
- `NoiseLevel` → `NoiseLevel`  [T= S= F= C=]
- `AirPollutantConcentration` → `AirPollutantConcentration`  [T= S= F= C=]
**Missed:** `BikeParkingUtilisation`, `BikeSpeed`
**Newly minted:** `CollisionRisk`, `ConflictPoints`, `BrakingFrequency`

## santos2022 · _Spatial Multi-Criteria Analysis for Road Segment Cycling Suitability Assessment_

**Matched:**
- `PopulationDensity` → `PopulationDensity`  [T= S= F≠ C≠]  ⟵ feature: GridCell ≠ Edge · criteria: Accessibility ≠ Suitability
- `Slope` → `Slope`  [T= S= F= C≠]  ⟵ criteria: Comfort/Safety ≠ Suitability
- `RoadType` → `RoadType`  [T= S= F= C≠]  ⟵ criteria: Safety ≠ Suitability
**Missed:** `DistanceToTransitFacility`
**Extra:** `DestinationDensity`

## ito2021 · _Comprehensive Bikeability Index_

**Matched:**
- `TrafficSignalDensity` → `IntersectionWithLightingDensity`  [T≠ S= F= C=]  ⟵ type: InfrastructuralMetric ≠ MorphologicalMetric
- `IntersectionDensity` → `IntersectionWithoutLightingDensity`  [T= S= F= C=]
- `CulDeSacDensity` → `CulDeSacDensity`  [T= S= F= C=]
- `Slope` → `Slope`  [T= S= F= C=]
- `DestinationDensity` → `DestinationDensity`  [T= S= F= C=]
- `LandUseMix` → `LandUseMix`  [T= S= F= C=]
- `AirPollutantConcentration` → `AirPollutantConcentration`  [T= S= F= C=]
- `DegreeOfGreenery` → `WaterSpaceShare`  [T= S= F= C=]
- `RoadType` → `RoadType`  [T= S= F= C=]
- `PotholePresence` → `PotholePresence`  [T= S= F= C=]
- `LightingPresence` → `LightingPresence`  [T= S= F= C=]
- `BikeLanePresence` → `BikeLanePresence`  [T= S= F= C=]
- `TransitFacilityDensity` → `TransitFacilityDensity`  [T= S≠ F= C=]  ⟵ scale: ratio ≠ nominal
- `SurfaceTypeAndCondition` → `PavementType`  [T≠ S= F= C=]  ⟵ type: CompositeMetric ≠ InfrastructuralMetric
- `StreetAmenityPresence` → `StreetAmenityPresence`  [T= S= F= C=]
- `UtilityPolePresence` → `UtilityPolePresence`  [T= S= F= C=]
- `BikeParkingPresence` → `BikeParkingPresence`  [T= S= F= C=]
- `RoadWidth` → `RoadWidth`  [T= S= F= C=]
- `SidewalkPresence` → `SidewalkPresence`  [T= S= F= C=]
- `CrosswalkPresence` → `CrosswalkPresence`  [T= S= F= C=]
- `CurbCutPresence` → `CurbCutPresence`  [T= S= F= C=]
- `PerceivedAttractivenessForCycling` → `PerceivedAttractivenessForCycling`  [T= S· F= C=]
- `PerceivedSpaciousness` → `PerceivedSpaciousness`  [T= S· F= C=]
- `PerceivedCleanliness` → `PerceivedCleanliness`  [T= S· F= C=]
- `PerceivedBuildingDesignAttractiveness` → `PerceivedBuildingDesignAttractiveness`  [T= S· F= C=]
- `PerceivedSafety` → `PerceivedSafety`  [T= S· F= C=]
- `PerceivedBeauty` → `PerceivedBeauty`  [T= S· F= C=]
- `PerceivedAttractivenessForLiving` → `PerceivedAttractivenessForLiving`  [T= S· F= C=]
- `MotorisedVehicleCount` → `MotorisedVehicleCount`  [T= S≠ F= C=]  ⟵ scale: ratio ≠ nominal
- `SideParkingPresence` → `SideParkingPresence`  [T= S= F= C=]
- `TrafficSignalOrStopSignPresence` → `TrafficSignalOrStopSignPresence`  [T= S= F= C=]
- `SpeedControlDevicePresence` → `SpeedControlDevicePresence`  [T= S= F= C=]
**Missed:** `GreenSpaceShare`
**Extra:** `BuildingCondition`, `WaterSpaceShare`

## abad2018 · _Bike Network Analysis (BNA) Score_

**Matched:**
- `SpeedLimit` → `SpeedLimit`  [T= S= F≠ C=]  ⟵ feature: Edge ≠ GridCell
- `ResidentialAreaPresence` → `ResidentialAreaPresence`  [T= S= F≠ C=]  ⟵ feature: Edge ≠ GridCell
- `CarLaneCount` → `CarLaneCount`  [T= S≠ F≠ C=]  ⟵ scale: ratio ≠ nominal · feature: Edge ≠ GridCell
- `Slope` → `Slope`  [T= S= F≠ C=]  ⟵ feature: Edge ≠ GridCell
**Missed:** `RoadType`
**Extra:** `LevelOfStress`, `BikeLanePresence`, `DestinationDensity`

## daraei2021 · _Bike Safety Risk Model_

**Matched:**
- `SpeedLimit` → `SpeedLimit`  [T= S= F= C=]
- `RoadWidth` → `RoadWidth`  [T= S= F= C=]
- `DistanceToIntersection` → `DistanceToIntersection`  [T= S= F= C=]
- `Slope` → `Slope`  [T= S= F= C=]
- `StreetTopology` → `Linearity`  [T= S= F= C=]
- `BikeLanePresence` → `BikeLanePresence`  [T= S= F= C=]
- `BetweenessCentrality` → `BetweenessCentrality`  [T= S· F≠ C=]  ⟵ feature: Edge ≠ PointOfInterest
**Newly minted:** `StreetTopology`

## boisjoly2019 · _Bicycle Network Performance Index_

**Matched:**
- `RouteDiversion` → `DetourFactor`  [T= S= F= C=]
- `RouteProportionOnFacilities` → `TravelOnBikeLaneAndRoadRatio`  [T= S= F= C≠]  ⟵ criteria: Connectivity ≠ Cost/Performance
**Extra:** `NetworkConnectivity`
**Newly minted:** `RouteDiversion`, `RouteProportionOnFacilities`, `NetworkConnectivity`

## reggiani2021 · _Bikeability Curves Methodology_

**Matched:**
- `Circuity` → `Sinuosity`  [T= S= F= C=]
- `RelativeDiscomfort` → `RelativeDiscomfort`  [T= S= F= C=]
**Extra:** `EdgeDiscomfort`, `NodeDiscomfort`, `PathLength`

## soltani2022 · _Space Syntax Bicycle Commuting Model_

**Matched:**
- `Connectivity` → `Connectivity`  [T= S· F= C≠]  ⟵ criteria: Connectivity ≠ Accessibility
- `GlobalDepth` → `Depth`  [T= S· F≠ C≠]  ⟵ feature: Edge ≠ Route · criteria: Directness ≠ Accessibility
- `Integration` → `Integration`  [T= S· F= C≠]  ⟵ criteria: Centrality ≠ Accessibility
- `Choice` → `Choice`  [T= S· F= C≠]  ⟵ criteria: Navigability ≠ Accessibility
**Missed:** `NodeDegree`
**Extra:** `PopulationDensity`, `LandUseMix`
**Newly minted:** `GlobalDepth`

## karolemeas2022 · _Bikeability Index_

**Matched:**
- `Slope` → `Slope`  [T= S= F= C=]
- `IntersectionDensity` → `IntersectionDensity`  [T= S= F= C=]
- `TrafficVolume` → `RoadType`  [T≠ S= F= C=]  ⟵ type: ModeMetric ≠ InfrastructuralMetric
- `SpeedLimit` → `MotorisedTrafficSpeed`  [T= S= F= C=]
- `DegreeOfGreenery` → `GreeneryPresence`  [T= S≠ F= C=]  ⟵ scale: nominal ≠ ordinal
- `BuildingCondition` → `UrbanVitalityPresence`  [T= S· F= C=]
- `DestinationDensity` → `DestinationDensity`  [T= S= F= C=]
- `DistanceToTransitFacility` → `TransitFacilityDensity`  [T= S= F= C=]
- `DistanceToBikeSharingStation` → `DistanceToBikeSharingStation`  [T= S= F= C=]
**Missed:** `RoadDensityInCentralArea`
**Extra:** `Centrality`

## codina2022 · _Barcelona Bikeability Index_

**Matched:**
- `CollisionAndBikeTripRatio` → `CollisionAndBikeTripRatio`  [T= S= F= C=]
- `DistanceToBikeLaneWithExclusiveness` → `DistanceToBikeLaneWithoutExclusiveness`  [T= S= F= C=]
- `DistanceToBikeLaneWithoutExclusiveness` → `DistanceToBikeSharingStation`  [T≠ S= F= C=]  ⟵ type: ContextualMetric ≠ InfrastructuralMetric
- `BikeLaneIntersectionDensity` → `BikeLaneIntersectionDensity`  [T= S= F= C=]
- `BikeParkingDensity` → `DistanceToBikeParking`  [T= S= F= C=]
- `Slope` → `Slope`  [T= S= F= C=]
**Missed:** `BikePathAndLaneIntersectionDensity`, `BikePathIntersectionDensity`
**Extra:** `BikeSharingStationDensity`
