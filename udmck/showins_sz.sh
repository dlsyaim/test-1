#!/bin/bash

cd /tmp

#Define func nf info check
function nf_check(){

echo > node.txt
echo > temp.txt


echo ""
echo "                                       Show all instances of nrf $NRF_ADDR"
echo ""
echo -e "\033[36mUUID\t\t\t\t\t\tNODE_TYPE\tSTATUS\t\t\tADDRESS\t\t\tNODE\033[0m"

curl -X GET "http://$NRF_ADDR:80/nnrf-nfm/v1/nf-instances" 2>/dev/null | python3 -mjson.tool | grep -i nf-instances/ | awk -F '[/\"]' '{print $10}' > line.txt

while read LINE 
do
    curl -X GET "http://$NRF_ADDR:80/nnrf-nfm/v1/nf-instances/$LINE" 2>/dev/null | python3 -m json.tool > temp.txt
    TYPE=$(cat temp.txt | grep -i \"nfType\")
    STATUS=$(cat temp.txt | grep -i \"nfStatus\")
    ADDRESS=$(cat temp.txt | grep -m 1 "[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\{1\}")
    FQDN=$(cat temp.txt | grep -m 1 -i \"fqdn\")
    
    
    TYPE=${TYPE//,/}
    TYPE=${TYPE// /}
    TYPE=${TYPE//\"/}
    TYPE=${TYPE//nfType:/}
    STATUS=${STATUS//,/}
    STATUS=${STATUS// /}
    STATUS=${STATUS//\"/}
    STATUS=${STATUS//nfStatus:/}
    ADDRESS=${ADDRESS//\"fqdn\":\ }
    ADDRESS=${ADDRESS//http:\/\//}
    ADDRESS=${ADDRESS//,/}
    ADDRESS=${ADDRESS// /}
    ADDRESS=${ADDRESS//\"ipv4Address\"\:}
    ADDRESS=${ADDRESS//\"/}
    FQDN=${FQDN// /}
    FQDN=${FQDN//,/}
    FQDN=${FQDN//\"/}
    FQDN=${FQDN//fqdn:/}
    FQDN=${FQDN%%\.*}
    
    if [[ $TYPE == "AMF" ]];then
        SET=$(cat temp.txt | grep -i set | cut -d':' -f 2)
        REGION=$(cat temp.txt | grep -i region | cut -d':' -f 2)
    fi
    
    if [[ $TYPE == "UDM" ]];then
        UDM_ADDR=$(cat temp.txt | grep -m 1 -i address | cut -d':' -f 2)
        UDM_ADDR=${UDM_ADDR//\"/}
        UDM_ADDR=${UDM_ADDR//,/}
        UDM_ADDR=${UDM_ADDR// /}
    fi

    if [[ $STATUS =~ "SUSPENDED" ]]; then
        echo -e "\033[7m$LINE\t\t$TYPE\t\t$STATUS\t\t$ADDRESS\t\t$FQDN\033[0m"
    else
        echo -e "$LINE\t\t$TYPE\t\t$STATUS\t\t$ADDRESS\t\t$FQDN"
    fi
    echo -e "$LINE\t\t$TYPE\t\t$STATUS\t\t$ADDRESS\t\t$FQDN" >> node.txt

done < line.txt
echo ""
}



#Define func nf discovery check
function dis_check(){

sed -i '1d' node.txt
echo -e "\033[36mDiscovery status:\033[0m"

#AMF
curl -s -X GET "http://$NRF_ADDR:80/nnrf-disc/v1/nf-instances?service-names=namf-evts&target-nf-type=AMF&requester-nf-type=AMF&amf-set-id=$SET&amf-region-id=$REGION" > amf.txt
n_ok AMF

#SMF
curl -s -X GET "http://$NRF_ADDR:80/nnrf-disc/v1/nf-instances?service-names=nsmf-pdusession&target-nf-type=SMF&requester-nf-type=AMF&dnn=Internet" > smf.txt
n_ok SMF

#AUSF
curl -s -X GET "http://$NRF_ADDR:80/nnrf-disc/v1/nf-instances?target-nf-type=AUSF&service-names=nausf-auth&requester-nf-type=AMF&supi=imsi-$IMSI" > ausf.txt
n_ok AUSF

#UDM
curl -s -X GET "http://$NRF_ADDR:80/nnrf-disc/v1/nf-instances?target-nf-type=UDM&service-names=nudm-sdm&requester-nf-type=AMF&supi=imsi-$IMSI" > udm.txt
n_ok UDM

#PCF
curl -s -X GET "http://$NRF_ADDR:80/nnrf-disc/v1/nf-instances?target-nf-type=PCF&service-names=npcf-am-policy-control&requester-nf-type=AMF&supi=imsi-$IMSI" > pcf.txt
n_ok PCF

#UDR
curl -s -X GET "http://$NRF_ADDR:80/nnrf-disc/v1/nf-instances?target-nf-type=UDR&service-names=nudr-dr&requester-nf-type=UDM&supi=imsi-$IMSI" > udr.txt
n_ok UDR

echo ""
}


#Define func subscription data check
function scrib_data_check(){
echo -e "\033[36mSubscription_data:\033[0m "

curl -s -X GET "http://$UDM_ADDR:81/nudm-sdm/v1/imsi-$IMSI/am-data" > am-data.txt 
n_ok am-data
curl -s -X GET "http://$UDM_ADDR:81/nudm-sdm/v1/imsi-$IMSI/sm-data" > sm-data.txt
n_ok sm-data
curl -s -X GET "http://$UDM_ADDR:81/nudm-sdm/v1/imsi-$IMSI/nssai" > nssai.txt
n_ok nssai
curl -s -X GET "http://$UDM_ADDR:81/nudm-sdm/v1/imsi-$IMSI/smf-select-data" > smf-select-data.txt
n_ok smf-select-data
echo ""
}

#print ok or nok
function n_ok(){
if [[ $? == 0 ]];then
    echo $1 is OK
else
    echo -e "\033[7m$1 is NOK\033[0m"
fi
}

#Define func auth data check
function auth_check(){
SUCI="suci-0-${IMSI:0:3}-${IMSI:3:2}-0000-0-0-${IMSI:5}"
curl -s -X POST "http://$UDM_ADDR/nausf-auth/v1/ue-authentications" -H "accept: application/3gppHal+json" -H "Content-Type: application/json" -d "{ \"supiOrSuci\": \"$SUCI\", \"servingNetworkName\": \"5G:mnc008.mcc460.3gppnetwork.org\"}" > auth.txt
cat auth.txt | grep -i 5G_AKA > /dev/null
n_ok "Authen data"
echo ""

}



# main func
function main(){
    nf_check
    dis_check
    scrib_data_check
    auth_check
}


#Variable evaluation

REGX="^((2(5[0-5]|[0-4][0-9]))|[0-1]?[0-9]{1,2})(\.((2(5[0-5]|[0-4][0-9]))|[0-1]?[0-9]{1,2})){3}$"
UUID="[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"

if [ $# == 2 ];then
    if [[ $2 =~ ^[0-9]{15} ]];then
        if [[ $1 =~ $REGX  ]];then
            IMSI=$2
            NRF_ADDR=$1
            main
        else
            echo "Address is not regular address"
        fi
    else
        echo "IMSI is not regular IMSI"
    fi
fi


if [ $# == 1 ];then
    NRF_ADDR="192.168.100.227"
    if [[ $1 =~ $UUID ]];then
        curl -X GET "http://$NRF_ADDR:80/nnrf-nfm/v1/nf-instances/$1" 2>/dev/null | python3 -m json.tool
    else
        echo "ID is not regular UUID"
    fi
fi


if [ $# == 0 ];then
    NRF_ADDR="192.168.100.227"
    IMSI="460070000000003"
    main
fi
