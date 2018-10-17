way(lat_min, lon_min, lat_max, lon_max)-> .w;
    (
        way.w["highway" ~ "trunk"];
        way.w["highway" ~ "primary"];
        way.w["highway" ~ "secondary"];
        way.w["highway" ~ "tertiary"];
        way.w["highway" ~ "unclassified"];
        way.w["highway" ~ "residential"];
        way.w["highway" ~ "service"];
        way.w["highway" ~ "footway"];
        way.w["highway" ~ "pedestrian"];
    ) -> ._;
(._; >;);