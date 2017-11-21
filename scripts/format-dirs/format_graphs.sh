#!/bin/bash
# $1 is the path to a collection of graphs
# $2 is the path to the template folder
# $3 is the path to output respec'd graphs
mkdir -p $3

for atlas_path in $(find $1 -mindepth 1 -maxdepth 1 -type d); do
    atlas_id=$(basename $atlas_path)
    echo "$atlas_id"
    opath="${3}/$atlas_id"
    mkdir -p $opath
    cp -r $2/* $opath/
    sed -i "s/RES/${atlas_id}/g" $opath/problemSchema.json
    g1path="$opath/data/raw_data/G1.edgelist"
    g2path="$opath/data/raw_data/G2.edgelist"
    cp ${atlas_path}/sub-0025864_ses-1* $g1path
    cp ${atlas_path}/sub-0025864_ses-2* $g2path
    python make_node_descriptions.py $g1path $g2path $opath/data/trainData.csv $opath/data/trainTargets.csv
done
