# Step 2 — candidate concepts (blind B vs guided G, aligned to v1)

_476 raw concepts → **264 clusters** (19 attested in ≥2 docs) · merge = same name OR definition-embedding cosine ≥ 0.88 · v1 via G canonical_match or lexical._

## Headline (robust = attested in ≥2 docs; singletons are the 1-doc tail, see CSV)
- **v1 coverage:** mining re-found **52** existing v1 concepts.
- **Novel candidates not in v1: 5 robust** (+ 165 singletons) — robust by facet: threshold 2, metric 1, metric_group 1, other 1.
- **Track split (robust):** G∩B 15 (both) · B∖G 4 (blind-only) · G∖B 0 (guided-only).
- **Anchoring-bias signal:** **3** robust novel concepts were found by BLIND mining but MISSED by guided — the v1 lens would have hidden them: `Level of Service (LOS)`, `Public transport and bicycle`, `cycling infrastructure`.
- **Evidence grounding:** 94% of raw concepts carry a quote verbatim-findable in their source text (normalized substring check). Ungrounded ones are paraphrased or hallucinated quotes — scrutinize during curation (`grounded` column in the CSV).

## criterion  (5 robust, 5 novel-singletons / 27 total)
- ⭐ **directness** [G∩B] docs=5 →v1:Directness · grp: bicycle infrastructure design principles, quality criteria
    variants: Coherence, coherence, connectivity, Directness, directness
    _The extent to which cycling routes provide the shortest or most efficient paths between origins and destinations._
- ⭐ **Lighting** [G∩B] docs=2 →v1:Security · grp: Infrastructure for high-level bicycle tourism, Qualitative design standards
    variants: Lighting, lighting
    _The presence and quality of illumination along cycling routes._
- ⭐ **proximity** [G∩B] docs=2 →v1:Directness · grp: Elements of Eﬀective Public Cycle Parking, InfrastructuralMetric
    variants: Max. distance, proximity
    _The closeness of the parking facility to the user's final destination._
- ⭐ **shelters for cyclists** [G∩B] docs=2 →v1:Comfort · grp: Infrastructure for high-level bicycle tourism, Qualitative design standards
    variants: covering/weather protection, Covering/weather protection, shelters for cyclists
    _Structures provided for cyclists to seek protection from weather conditions._
- ⭐ **visibility** [G∩B] docs=2 →v1:Quality · grp: Elements of Eﬀective Public Cycle Parking
    variants: visibility, Visibility
    _The degree to which a facility or road user can be seen by others._
- **bicycle infrastructure design principles** [B∖G] docs=1 **NOVEL**
    _These are five internationally recognized criteria—safety, comfort, attractiveness, directness, and coherence—that inclusive cycling infrast_
- **control and enforcement program** [B∖G] docs=1 **NOVEL** · grp: design parameters
    _Administrative and physical measures to ensure the lane is used only by authorized vehicles and that traffic rules are followed._
- **criterion** [B∖G] docs=1 **NOVEL**
    _A criterion is a qualitative assessment objective, such as safety or accessibility, that requires quantifiable observations._
- **diversiﬁcation** [G∩B] docs=1 **NOVEL** · grp: Elements of Eﬀective Public Cycle Parking
    variants: diversification, diversiﬁcation
    _The provision of a variety of parking types to accommodate different user needs and preferences._
- **E-bike charging infrastructure** [G∖B] docs=1 **NOVEL**
    _The availability of electrical outlets to charge e-bike batteries at the parking location._
  _+ 17 v1-confirmed single-doc mentions (see candidates.csv)._

## metric  (8 robust, 95 novel-singletons / 155 total)
- ⭐ **Safety** [G∩B] docs=19 →v1:Bikeability · grp: Access Sheds and Networks, bicycle infrastructure design principles
    variants: accessibility, Accessibility, Aesthetic and attractiveness, attractiveness, Attractiveness, attractiveness indexes, BEQI (Bicycle Environmental Quality Index), BEQI(Bicycle Environmental Quality Index)
    _The degree to which a cycling environment protects users from accidents and injuries._
- ⭐ **Dynamic comfort index (DCI)** [G∩B] docs=5 →v1:Smoothness · grp: Comfort assessment methods, CompositeMetric
    variants: Cycling Comfort Index, dynamic comfort index, Dynamic Comfort Index, Dynamic Comfort Index (DCI), Dynamic comfort index (DCI), Dynamic Cycling Comfort (DCC), Dynamic cycling comfort (DCC), IRI (International Roughness Index)
    _A metric evaluating vibration caused by pavement surface properties to assess cycling comfort._
- ⭐ **bicycle parking** [G∩B] docs=4 →v1:Amenity · grp: Cycling infrastructure, InfrastructuralMetric
    variants: bicycle parking, Bicycle parking
    _Facilities provided at transit stations for the secure storage of bicycles._
- ⭐ **Topography** [G∩B] docs=4 →v1:MorphologicalMetric · grp: ContextualMetric, Exogenous Factors
    variants: Slope, slope, Topography, topography
    _The physical grade or slope of the terrain which affects the physical effort required by the cyclist._
- ⭐ **cycling ridership** [G∩B] docs=3 →v1:Performance · grp: ModeMetric
    variants: bicycle modal share, cycling ridership, cycling uptake, Cycling uptake
    _This indicator tracks the growth or level of cycling participation within a city._
- ⭐ **Level of Service (LOS)** [B∖G] docs=3 **NOVEL** · grp: Investigated characteristics and attributes of network affecting users’ choice
    variants: Level of Service (LOS), Level of service (LOS)
    _A numerical stratification used to categorize performance measures of quality of service._
- ⭐ **prêdkoœæ do projektowania** [G∩B] docs=2 →v1:DesignSpeed · grp: Basic parameters of bicycle infrastructure, InfrastructuralMetric
    variants: design speed, prêdkoœæ do projektowania
    _The speed value used as a basis for determining geometric parameters of bicycle infrastructure to ensure safety and consistent riding condit_
- ⭐ **Traffic volume** [B∖G] docs=2 →v1:TrafficVolume · grp: Safety
    variants: Traffic volume, traffic volume
    _This indicator tracks the density of motorized vehicles, which is inversely related to the perceived safety of cycling._
- **accessibility deserts** [G∩B] docs=1 **NOVEL** · grp: CompositeMetric, Equity metrics
    variants: Accessibility deserts, accessibility deserts
    _Areas identified as having low accessibility combined with high socioeconomic disadvantage._
- **Active Commuter Route Environment (ACRE)** [B∖G] docs=1 **NOVEL** · grp: Bikeability Index (BI)
    _A framework incorporating self-reported data to evaluate commuting routes._
- **Advisory cycle lane** [G∖B] docs=1 **NOVEL** · grp: InfrastructuralMetric
    _A lane intended for cyclists but not legally restricted, often used on narrow roads where mixing with motor vehicles is required._
- **appreciation of design** [B∖G] docs=1 **NOVEL** · grp: design appreciations
    _A qualitative assessment of how well infrastructure design features meet the preferences and needs of cyclists._
- **Area-Wide Bikeability Assessment Model** [G∖B] docs=1 **NOVEL** · grp: CompositeMetric
    _A model used to assess the bikeability of urban zones or areas rather than individual segments._
- **Area-wide bikeability assessment model (ABAM)** [B∖G] docs=1 **NOVEL** · grp: Bikeability Index (BI)
    _A zone-based method using an Analytic Network Process framework to evaluate the friendliness of an area to biking._
- **Availability** [B∖G] docs=1 **NOVEL** · grp: Cycle Infrastructure
    _This indicator tracks the existence of specific cycling facilities like bicycle lanes within a given area or route._
- **Behavior** [B∖G] docs=1 **NOVEL** · grp: Safety
    _These indicators capture the attitudes and behaviors of cyclists and drivers regarding safety and enforcement._
- **behavioral risk indicator** [G∩B] docs=1 **NOVEL** · grp: Comfort assessment methods, ContextualMetric
    _A method employed in studies to evaluate behavioral risks associated with cycling._
- **bent-out crossings** [G∩B] docs=1 **NOVEL** · grp: InfrastructuralMetric, protected intersections and priority crossings
    variants: bent-out crossings, bent-out cycle paths
    _A crossing design that diverts the cycle path away from the main carriageway at intersections to improve visibility and allow vehicles to yi_
- **Bicycle Sharing System** [B∖G] docs=1 **NOVEL** · grp: Cycle Infrastructure
    _This indicator evaluates the availability and spatial coverage of bicycle sharing systems within an urban area._
- **Bicycle traffic volume** [B∖G] docs=1 **NOVEL** · grp: Safety
    _This indicator quantifies the volume of bicycle traffic, which contributes to the 'safety-in-numbers' effect._
- **Bicycle-Friendly Accommodation Facility Certificate** [G∩B] docs=1 **NOVEL** · grp: CompositeMetric
    _A formal certification issued by the Turkish Ministry of Culture and Tourism to standardize and recognize accommodation services for cyclist_
- **bike box** [G∩B] docs=1 **NOVEL** · grp: InfrastructuralMetric, Infrastructure
    variants: Bike box, bike box
    _A designated space at the head of a traffic lane that allows cyclists to wait in a highly visible location during red signal phases._
- **Bike Composite Index** [G∖B] docs=1 **NOVEL** · grp: CompositeMetric
    _An index integrating attractiveness factors like network density and safety factors like crash risk to evaluate bike-friendly planning._
- **Bike Composite Index (BCI)** [B∖G] docs=1 **NOVEL** · grp: Investigated characteristics and attributes of network affecting users’ choice
    _An index that combines network density, land use, slope, crash risk, and infrastructure features._
- **Bike Score®** [B∖G] docs=1 **NOVEL** · grp: BI
    _A tool that models the relationship between bikeability and cycling mode share._
- **bike share** [G∖B] docs=1 **NOVEL** · grp: ModeMetric
    _A shared bicycle service that allows users to pick up and drop off bicycles at various locations, often used for first/last mile connections_
- **Bivariate Local Moran’s I** [G∩B] docs=1 **NOVEL** · grp: Equity metrics, GraphMetric
    _A spatial statistic used to identify where low accessibility systematically coincides with social disadvantage._
- **calculated accessibility** [B∖G] docs=1 **NOVEL**
    _An objective measure of the ability to reach destinations based on spatial and transport data._
- **Cargo bikes** [B∖G] docs=1 **NOVEL** · grp: Qualitative design standards
    _The requirement to provide dedicated space for larger cargo bicycles._
- **City Cycle Infrastructure Score (CCIS)** [B∖G] docs=1 **NOVEL** · grp: BLOS
    _A scoring system based on infrastructure audits to evaluate bicycle facilities._
- **Climate** [B∖G] docs=1 **NOVEL** · grp: Exogenous Factors
    _Weather and seasonal conditions that impact the decision to cycle and user comfort._
- **Collisions** [B∖G] docs=1 **NOVEL** · grp: Safety
    _This indicator identifies crash hot spots or the density of accidents to assess the safety of the cycling environment._
- **colored pavements** [G∩B] docs=1 **NOVEL** · grp: InfrastructuralMetric, Infrastructure
    variants: Colored pavement, colored pavements, spot treatment, Spot treatment
    _A technique for applying a distinctive, contrasting surface color to bicycle facilities to improve visibility and reinforce priority._
- **competition-based measures** [B∖G] docs=1 **NOVEL** · grp: Accessibility metrics
    _Models like the Floating Catchment Area that account for the competition between users for limited opportunities._
- **Composite Index of Accessibility** [B∖G] docs=1 **NOVEL** · grp: Accessibility metrics
    _A metric combining passive and active accessibility._
- **Concentration Index** [G∩B] docs=1 **NOVEL** · grp: CompositeMetric, Equity metrics
    variants: Concentration Index, Gini coefficient
    _A statistical index used to measure the inequality of accessibility distribution across a population._
- **connectivity and intersections** [B∖G] docs=1 **NOVEL** · grp: Accessibility
    _The density and layout of street intersections within a network._
- **continuous path crossings** [G∖B] docs=1 **NOVEL** · grp: InfrastructuralMetric
    _A crossing design where the bicycle path maintains a straight alignment across side streets to prioritize active transport._
- **Conﬂicts** [B∖G] docs=1 **NOVEL** · grp: Safety
    _These indicators identify locations where cycling paths intersect with other activities, such as bus stops or car parking, that may disrupt _
- **corridor treatment** [G∩B] docs=1 **NOVEL** · grp: InfrastructuralMetric, Infrastructure
    variants: corridor treatment, Corridor treatment
    _The application of color along the entire length of a cycle facility to enhance visibility and compliance._
- **Criminality** [B∖G] docs=1 **NOVEL** · grp: Safety
    _This indicator assesses the impact of crime rates or perceived security on the willingness of children to cycle._
- **Cycle street** [G∖B] docs=1 **NOVEL** · grp: InfrastructuralMetric
    _A street where cyclists have priority in a speed-restricted environment shared with motor vehicles._
- **Cyclist Routing Algorithm for Network Connectivity** [G∖B] docs=1 **NOVEL** · grp: CompositeMetric
    _A simulation tool that balances travel time and traffic stress to model cyclist route preferences._
- **DataSource** [B∖G] docs=1 **NOVEL**
    _Data source identifies the origin of the information used to calculate a metric, such as Open Street Maps._
- **Degree of urbanisation** [B∖G] docs=1 **NOVEL** · grp: Connectivity and urbanisation
    _This indicator reflects population density, which is associated with social interaction and access to services, impacting active travel._
- **destination** [B∖G] docs=1 **NOVEL** · grp: Land use
    _The presence and proximity of locations such as services, shops, or transit facilities that attract cyclists._
- **different types of tracks** [B∖G] docs=1 **NOVEL** · grp: Infrastructure for high-level bicycle tourism
    _The specific physical configuration or design of the cycling path surface._
- **Dynamic Cycling Comfort** [G∖B] docs=1 **NOVEL** · grp: CompositeMetric
    _A system that uses accelerometers on bicycles to measure real-time vibration levels experienced by cyclists._
- **E-bike charging** [B∖G] docs=1 **NOVEL** · grp: Qualitative design standards
    _The provision of electrical infrastructure to charge electric bicycles._
- **enforcement and control** [G∖B] docs=1 **NOVEL** · grp: InfrastructuralMetric
    _The set of measures and monitoring activities used to ensure compliance with traffic regulations._
- **Environment** [B∖G] docs=1 **NOVEL** · grp: Macro-attributes or factors
    _A measurement of environmental features like greenery, pedestrian areas, and noise levels._
- **evaluation metric** [B∖G] docs=1 **NOVEL**
    _An evaluation metric is a directly measurable network-related characteristic used to quantify an evaluation criterion._
- **existence and width of bike lanes** [B∖G] docs=1 **NOVEL** · grp: Infrastructure
    _The presence and physical dimensions of designated bicycle lanes._
- **filtered permeability** [G∩B] docs=1 **NOVEL** · grp: InfrastructuralMetric, quietways and low-traffic neighbourhoods
    _A method of restricting motor vehicle through-traffic while allowing passage for pedestrians and cyclists._
- **Geometric design features (layout and cross sections)** [B∖G] docs=1 **NOVEL** · grp: Cycle Infrastructure
    _This criterion assesses the physical dimensions of cycle paths and their relationship to motorized traffic and intersections._
- **gravity-based accessibility measures** [B∖G] docs=1 **NOVEL** · grp: Accessibility metrics
    _A model that weights reachable opportunities based on the travel cost to reach them._
- **impedance** [B∖G] docs=1 **NOVEL** · grp: Access Sheds and Networks
    _A measure of the resistance encountered by a traveler, such as high-stress routes or steep topography, which reduces the effective access sh_
- **independent cycles count** [G∖B] docs=1 **NOVEL** · grp: GraphMetric
    _A count of the number of independent cycles within a graph structure._
- **infrastructure, information and services needed at intermodal nodes** [B∖G] docs=1 **NOVEL** · grp: Transport services and intermodality
    _A combined set of requirements for facilities and data at locations where different modes of transport connect._
- **Infrastructures** [B∖G] docs=1 **NOVEL** · grp: Macro-attributes or factors
    _A measurement of physical road features such as pavement quality and signage._
- **International Roughness Index (IRI)** [B∖G] docs=1 **NOVEL** · grp: vibration or roughness index
    _A metric used to quantify road surface roughness and pavement quality._
- **intersections and roundabouts** [B∖G] docs=1 **NOVEL** · grp: Infrastructure for high-level bicycle tourism
    _The design and safety features of junctions where cycle routes meet other traffic._
- **Landscape Aesthetics (green and aquatic features)** [B∖G] docs=1 **NOVEL** · grp: Surrounding Environment
    _This criterion measures the presence of green and aquatic elements that improve the cycling experience and well-being._
- **Lightning** [B∖G] docs=1 **NOVEL** · grp: Safety
    _This indicator assesses the presence of street lighting to improve visibility and safety during non-daylight hours._
- **low-traffic neighbourhoods** [G∩B] docs=1 **NOVEL** · grp: InfrastructuralMetric, infrastructure themes
    _Precinct-scale areas where through-traffic is restricted to create safe, low-stress environments for active travel._
- **maintenance** [B∖G] docs=1 **NOVEL** · grp: Infrastructure for high-level bicycle tourism
    _The ongoing care and repair of cycling infrastructure to ensure usability._
- **Multimodal features (Interface and parking)** [B∖G] docs=1 **NOVEL** · grp: Cycle Infrastructure
    _This criterion measures the connectivity between cycling and public transport, as well as the availability of bicycle parking._
- **Natural elements** [B∖G] docs=1 **NOVEL** · grp: Surrounding environment
    _This indicator tracks the presence of trees, parks, and bodies of water that provide aesthetic or functional benefits like shade._
- **Network features** [B∖G] docs=1 **NOVEL** · grp: Accessibility
    _These indicators assess the physical layout of the network to minimize travel distance and maximize connectivity between nodes._
- **Obstacles on bicycle paths** [B∖G] docs=1 **NOVEL** · grp: Cycling infrastructure
    _This indicator identifies physical barriers or obstructions that impede the ease of cycling and create safety hazards._
- **Palma ratio** [G∩B] docs=1 **NOVEL** · grp: CompositeMetric, Equity metrics
    _A ratio comparing the accessibility shares of the most advantaged and least advantaged groups._
- **Pavement Conditions** [B∖G] docs=1 **NOVEL** · grp: Infrastructure
    _The quality of the road surface and the presence of safety devices like speed humps._
- **perceived safety index** [B∖G] docs=1 **NOVEL** · grp: safety
    _A calculated metric used to quantify the level of safety perceived by cyclists across different routes._
- **Physical effort** [G∖B] docs=1 **NOVEL** · grp: ContextualMetric
    _An impedance measure that accounts for topography and power demand rather than just travel time._
- **Pollution (Air quality and Noise)** [B∖G] docs=1 **NOVEL** · grp: Surrounding Environment
    _This criterion assesses the exposure of cyclists to air pollutants and noise generated by traffic._
- **poszerzenie dróg dla rowerów na ³ukach** [G∩B] docs=1 **NOVEL** · grp: InfrastructuralMetric
    _The additional width added to a bicycle path on curves to accommodate the space required for a cyclist's tilt and movement._
- **Proportion of municipality area covered by BSS** [G∩B] docs=1 **NOVEL** · grp: Bike sharing systems, InfrastructuralMetric
    _This indicator measures the percentage of a municipality's total area served by a bike sharing system._
- **Quality of bicycle infrastructure at intersections** [B∖G] docs=1 **NOVEL** · grp: Cycling infrastructure
    _This indicator evaluates the presence and safety features of cycling infrastructure specifically at road intersections._
- **Quantity** [B∖G] docs=1 **NOVEL** · grp: Cycle Infrastructure
    _This indicator quantifies the amount of cycling infrastructure available, often expressed as length per unit area or percentage of the total_
- **road typology** [B∖G] docs=1 **NOVEL**
    _The classification of a road based on its function, such as residential, distributor, or main road._
- **route signposting** [B∖G] docs=1 **NOVEL** · grp: Infrastructure for high-level bicycle tourism
    _The system of visual markers and signs used to guide cyclists along a route._
- **safety-in-numbers effect** [B∖G] docs=1 **NOVEL**
    _An observed relationship where the risk of collision for a cyclist or pedestrian decreases as the total volume of people walking or cycling _
- **School site entrance location and school zones signage** [B∖G] docs=1 **NOVEL** · grp: Safety
    _This indicator tracks the location of school entrances and the presence of signage to create safe school zones._
- **scoring and weighting system** [B∖G] docs=1 **NOVEL**
    _This method assigns points to indicators and applies weights based on their perceived importance to calculate a total index score._
- **Service measures** [B∖G] docs=1 **NOVEL**
    _Specific performance metrics utilized to define the level of service._
- **Shared bus-bike lanes** [G∖B] docs=1 **NOVEL** · grp: InfrastructuralMetric
    _A road lane designated for buses that also permits bicycle traffic._
- **Sharing policy** [B∖G] docs=1 **NOVEL** · grp: Infrastructure
    _The regulatory and design approach determining where cyclists are permitted to ride within the network._
- **Short-/long-term parking** [B∖G] docs=1 **NOVEL** · grp: Qualitative design standards
    _A classification of parking based on the expected duration of stay._
- **Signage/ signalling** [B∖G] docs=1 **NOVEL** · grp: Cycling infrastructure
    _This indicator accounts for the availability and readability of signs intended to guide or regulate bicycle traffic._
- **Sociodemographic Aspects** [B∖G] docs=1 **NOVEL** · grp: Exogenous Factors
    _Personal characteristics of the cyclist, such as age and gender, that correlate with different cycling behaviors and comfort needs._
- **Spatial Availability** [G∖B] docs=1 **NOVEL** · grp: CompositeMetric
    _A metric that reformulates accessibility with competition by ensuring the sum of available opportunities equals the total system opportuniti_
- **spatial entity representations** [B∖G] docs=1 **NOVEL**
    _These are the spatial features, such as nodes or edges, to which metrics are mapped._
- **Street connectivity/ Intersection density** [B∖G] docs=1 **NOVEL** · grp: Connectivity and urbanisation
    _This indicator assesses the density of intersections and the availability of multiple route options for cyclists._
- **Theil index** [B∖G] docs=1 **NOVEL** · grp: Equity metrics
    _A measure that decomposes accessibility disparities into within-group and between-group components._
- **Traffic control devices and speed limiting measures** [B∖G] docs=1 **NOVEL** · grp: Safety
    _This indicator tracks the location of devices designed to manage traffic speeds and improve safety for vulnerable road users._
- **Trafﬁc** [B∖G] docs=1 **NOVEL** · grp: Safety
    _These indicators measure traffic volume, speed, and composition to determine the level of stress or service for cyclists._
- **Traﬃc enforcement** [B∖G] docs=1 **NOVEL** · grp: Infrastructure
    _The use of signs, signals, and markings to regulate traffic and provide guidance to cyclists._
- **Trip-End Facility** [B∖G] docs=1 **NOVEL** · grp: Infrastructure
    _Facilities located at the destination of a trip, such as parking or showers, that influence the decision to cycle._
- **Type of bicycle infrastructure** [B∖G] docs=1 **NOVEL** · grp: Cycling infrastructure
    _This indicator distinguishes between different physical configurations of cycling facilities, such as shared streets versus physically separ_
- **Typology** [B∖G] docs=1 **NOVEL** · grp: Cycle Infrastructure
    _This indicator classifies infrastructure based on the degree of separation from other traffic, such as shared lanes versus dedicated paths._
- **Visitors/permanent users** [B∖G] docs=1 **NOVEL** · grp: Qualitative design standards
    _A classification of parking based on the user type._
- **walkable catchment** [B∖G] docs=1 **NOVEL** · grp: Access Sheds and Networks
    variants: bike sheds, walkable catchment
    _The distance a person is willing to walk to reach a transit stop or station._
- **Weight** [B∖G] docs=1 **NOVEL**
    _Weighting is a mechanism to reflect the varying importance of different metrics or criteria in an evaluation._
  _+ 52 v1-confirmed single-doc mentions (see candidates.csv)._

## metric_group  (2 robust, 34 novel-singletons / 40 total)
- ⭐ **Land use** [G∩B] docs=3 →v1:ContextualMetric · grp: Accessibility
    variants: Land use, land-use
    _These indicators measure the proximity and density of origins and destinations, such as residential areas and workplaces, to support utilita_
- ⭐ **Public transport and bicycle** [B∖G] docs=2 **NOVEL**
    variants: Public transport and bicycle, Transport services and intermodality
    _This category addresses the integration of cycling with transit systems to extend catchment areas and facilitate longer trips._
- **access sheds** [G∩B] docs=1 **NOVEL** · grp: Access Sheds and Networks, ContextualMetric
    variants: access sheds, pedestrian sheds, walk sheds
    _An access shed is the geographic area around a transit stop or station that a person would reasonably travel to reach it._
- **Additional Services** [B∖G] docs=1 **NOVEL**
    _A category of optional criteria that facilities can choose to implement to earn points toward certification._
- **Bicycle Safety Index (BSI)** [B∖G] docs=1 **NOVEL**
    _A safety evaluation method that uses quantitative models to assess risks related to infrastructure design and traffic._
- **bicycle sharing systems** [G∖B] docs=1 **NOVEL** · grp: InfrastructuralMetric
    _Indicators related to the availability and performance of shared bicycle services._
- **Comfort and Sense of Place** [B∖G] docs=1 **NOVEL**
    _A thematic category for indicators related to passenger comfort and the aesthetic/cultural quality of the station area._
- **Composite Metrics** [B∖G] docs=1 **NOVEL** · grp: thematic metric classes
    _Composite metrics represent complex measurements, often based on theoretical frameworks, that combine multiple factors._
- **Connectivity and urbanisation** [B∖G] docs=1 **NOVEL**
    _This domain covers the spatial arrangement of streets and the density of population or activities that influence cycling feasibility._
- **Contextual Metrics** [B∖G] docs=1 **NOVEL** · grp: thematic metric classes
    _Contextual metrics incorporate external information like land-use or socio-economic conditions to analyze broader network implications._
- **Cycle Infrastructure** [B∖G] docs=1 **NOVEL**
    _This domain encompasses the physical supply, design, and quality of cycling-specific infrastructure and its integration with other transport_
- **economy** [B∖G] docs=1 **NOVEL**
    _A thematic category encompassing indicators related to the financial and economic outcomes of infrastructure projects._
- **Effective Wayfinding** [B∖G] docs=1 **NOVEL**
    _A thematic category for indicators related to signage, maps, and information that help users navigate to and through transit facilities._
- **electric bicycles** [G∖B] docs=1 **NOVEL** · grp: ModeMetric
    _Indicators accounting for the presence and impact of electric-assist bicycles on network performance._
- **Elements of Eﬀective Public Cycle Parking** [B∖G] docs=1 **NOVEL**
    _A framework of design principles used to guide the planning of public cycle parking facilities._
- **Exogenous Factors** [B∖G] docs=1 **NOVEL**
    _A category of external variables that influence the cycling experience but are outside the direct control of planners._
- **Fundamental relationship** [B∖G] docs=1 **NOVEL** · grp: Bicycle flow
    _The fundamental relationship is a concept used to relate speed, density, and flow for traffic modeling._
- **Graph Metrics** [B∖G] docs=1 **NOVEL** · grp: thematic metric classes
    _Graph metrics assess the connectivity and efficiency of the network from a structural perspective._
- **Infrastructural Metrics** [B∖G] docs=1 **NOVEL** · grp: thematic metric classes
    _Infrastructural metrics refer to the physical properties of the network infrastructure._
- **Infrastructure for high-level bicycle tourism** [B∖G] docs=1 **NOVEL**
    _A category encompassing physical road elements and facilities designed to support high-quality cycling experiences._
- **Infrastructure for information** [B∖G] docs=1 **NOVEL**
    _This category includes maps, apps, and digital platforms that provide information to cyclists._
- **Infrastructure for tourism** [B∖G] docs=1 **NOVEL**
    _This category focuses on routes designed for recreational cycling and holiday travel._
- **Infrastructure for transport of goods by bicycle and taxi bikes** [B∖G] docs=1 **NOVEL**
    _This category covers infrastructure supporting cargo delivery by bike and taxi-bike services._
- **Infrastructure that supports bicycle users** [B∖G] docs=1 **NOVEL**
    _This category includes retail, repair, and physical aids like ramps to assist cyclists._
- **Institutional support** [B∖G] docs=1 **NOVEL**
    _This category covers administrative bodies like bicycle offices that manage networks and promote cycling culture._
- **Macro-attributes or factors** [B∖G] docs=1 **NOVEL**
    _This group encompasses external elements such as infrastructure, comfort, and safety that influence user choices._
- **Mandatory Services** [B∖G] docs=1 **NOVEL**
    _A category of essential criteria that an accommodation facility must fulfill to qualify for certification._
- **MeasurementScale** [B∖G] docs=1 **NOVEL**
    _Measurement scale defines the type of data (nominal, ordinal, interval, or ratio) used by a metric._
- **Modal interaction** [B∖G] docs=1 **NOVEL** · grp: Bicycle flow
    _Modal interaction measures how different transport modes interact on road facilities and affect cyclist comfort._
- **Mode Metrics** [B∖G] docs=1 **NOVEL** · grp: thematic metric classes
    _Mode metrics measure the interactions between different transport modes, such as cars and bikes._
- **Morphological Metrics** [B∖G] docs=1 **NOVEL** · grp: thematic metric classes
    _Morphological metrics relate to the geometric configuration and physical properties of the bike network._
- **movement and place** [G∩B] docs=1 **NOVEL**
    _A strategy that balances the function of streets as conduits for travel with their role as spaces for social and economic interaction._
- **Parking** [B∖G] docs=1 **NOVEL**
    _This category encompasses the provision of secure, sheltered or unsheltered bicycle parking._
- **Qualitative design standards** [B∖G] docs=1 **NOVEL**
    _A set of criteria focused on the functional and design characteristics of bicycle parking facilities._
- **ScoringFunction** [B∖G] docs=1 **NOVEL**
    _A scoring function is a method used to unify metrics with diverse measurement scales into a comparable format._
- **space syntax** [G∖B] docs=1 **NOVEL** · grp: MorphologicalMetric
    _A set of techniques for analyzing the spatial configuration of urban networks and its impact on movement flows._
  _+ 4 v1-confirmed single-doc mentions (see candidates.csv)._

## data_modality  (1 robust, 2 novel-singletons / 8 total)
- ⭐ **surveys** [G∩B] docs=2 →v1:survey
    _Subjective measurement method using questionnaires to gather user feedback and perceptions._
- **instrumented probe bicycle** [G∖B] docs=1 **NOVEL**
    _A bicycle equipped with various sensors to collect objective data on infrastructure conditions._
- **smart bicycle lights** [G∖B] docs=1 **NOVEL**
    _Sensor-equipped bicycle lights used as a platform for collecting vibration and journey data._
  _+ 5 v1-confirmed single-doc mentions (see candidates.csv)._

## representation_feature  (0 robust, 2 novel-singletons / 3 total)
- **cycle network** [B∖G] docs=1 **NOVEL**
    _A cycle network is an interconnected set of safe and direct cycling routes covering a given area or city._
- **unit of analysis** [B∖G] docs=1 **NOVEL**
    _The unit of analysis defines the geographical scope of the assessment, ranging from street segments to entire cities._
  _+ 1 v1-confirmed single-doc mentions (see candidates.csv)._

## scoring  (0 robust, 3 novel-singletons / 3 total)
- **non-mandatory criteria (“nice to have”)** [B∖G] docs=1 **NOVEL**
    _Desirable quality standards that improve a route but are not strictly required for baseline quality assessment._
- **points-based evaluation system** [G∩B] docs=1 **NOVEL** · grp: Additional Services
    _A quantitative method used to assess a facility's eligibility for certification by summing points earned from optional service criteria._
- **strictly mandatory criteria (“must have”)** [B∖G] docs=1 **NOVEL**
    _Essential quality standards that must be met for a route to be considered acceptable, which cannot be offset by other positive features._

## weighting  (0 robust, 1 novel-singletons / 1 total)
- **Analytic Hierarchy Process** [G∖B] docs=1 **NOVEL**
    _A structured technique for organizing and analyzing complex decisions, used here to weight bikeability indicators._

## aggregation  (0 robust, 2 novel-singletons / 2 total)
- **matrix-based methods** [G∩B] docs=1 **NOVEL**
    _A decision framework that combines multiple variables like speed and volume to categorize the required infrastructure type._
- **vibration and visual inspection** [B∖G] docs=1 **NOVEL** · grp: Comfort assessment methods
    _This approach pairs sensor-recorded vibration data with manual or digital visual checks to verify the cause of surface roughness._

## threshold  (2 robust, 1 novel-singletons / 3 total)
- ⭐ **must have** [G∩B] docs=2 **NOVEL**
    _A mandatory requirement or minimum standard that must be met for a facility to be considered acceptable._
- ⭐ **nice to have** [G∩B] docs=2 **NOVEL**
    _A non-mandatory criterion that provides additional value but is not strictly required for basic functionality._
- **threshold** [G∖B] docs=1 **NOVEL**
    _A specific value of a metric used to determine the requirement for a specific type of infrastructure._

## other  (1 robust, 20 novel-singletons / 22 total)
- ⭐ **cycling infrastructure** [B∖G] docs=2 **NOVEL** · grp: design parameters
    variants: cycling infrastructure, Cycling infrastructure
    _The specific physical configuration or layout provided for cyclists within a shared lane._
- **Accueil Vélo** [B∖G] docs=1 **NOVEL**
    _A French national accreditation program that guarantees a high standard of hospitality for cyclists._
- **alignment within the SBBL** [B∖G] docs=1 **NOVEL** · grp: design parameters
    _The lateral positioning of the bicycle path or space relative to the bus lane._
- **Bett+Bike** [B∖G] docs=1 **NOVEL**
    _A long-standing German certification scheme for bicycle-friendly accommodations used across several European countries._
- **Bicycle parking requirements** [G∩B] docs=1 **NOVEL**
    variants: Bicycle parking requirements, bicycle parking requirements
    _Mandatory standards in building codes that dictate the quantity and quality of bicycle storage facilities required for new or renovated buil_
- **Bike Friendly** [B∖G] docs=1 **NOVEL**
    _A Greek certification label awarded to tourism stakeholders including accommodation facilities and municipalities._
- **Colored overlay** [B∖G] docs=1 **NOVEL**
    _Applying a colored layer on top of an existing pavement surface._
- **Crime Prevention Through Environmental Design (CPTED)** [B∖G] docs=1 **NOVEL** · grp: Personal Safety and Security
    _Design techniques that create an environment conducive to safety and discourage criminal activity._
- **Cyclists Welcome** [B∖G] docs=1 **NOVEL**
    _A British certification program administered by Cycling UK for various tourism businesses including accommodations._
- **evaluation approach** [B∖G] docs=1 **NOVEL**
    _An evaluation approach is a research paper, guideline, or tool that assesses bike networks using a combination of metrics and qualitative cr_
- **GIS (Geographic Information System)** [B∖G] docs=1 **NOVEL**
    _A technological tool used to map and analyze geospatial data for urban indicators._
- **hook turn storage box** [B∖G] docs=1 **NOVEL** · grp: Infrastructure
    _A designated area within an intersection that allows cyclists to perform two-stage left turns._
- **individual and social** [B∖G] docs=1 **NOVEL**
    _This component considers how personal characteristics and social dynamics influence accessibility._
- **Interested but Concerned** [G∩B] docs=1 **NOVEL**
    variants: Interested but concerned, Interested but Concerned
    _A population cohort that is willing to cycle but is deterred by perceived safety risks and traffic concerns._
- **post-certification inspections** [G∖B] docs=1 **NOVEL**
    _Ongoing or periodic assessments conducted after the initial certification to ensure continued compliance with standards._
- **Quality Plus** [B∖G] docs=1 **NOVEL** · grp: Bett+Bike
    _An advanced level of certification within the Bett+Bike program requiring additional criteria beyond the basic standard._
- **Shared bus-bike lanes (SBBLs)** [B∖G] docs=1 **NOVEL**
    _A bus lane where cyclists are permitted to travel alongside buses._
- **Surface course coloring** [B∖G] docs=1 **NOVEL**
    _Coloring the pavement material itself during the manufacturing or pouring process._
- **temporal** [B∖G] docs=1 **NOVEL**
    _This component accounts for how accessibility changes based on time-dependent factors._
- **threshold values** [B∖G] docs=1 **NOVEL**
    _Specific numerical limits for traffic speed or volume that dictate which type of cycling infrastructure must be implemented._
- **transport** [B∖G] docs=1 **NOVEL**
    _This component measures the difficulty or cost of traveling between locations._
  _+ 1 v1-confirmed single-doc mentions (see candidates.csv)._
