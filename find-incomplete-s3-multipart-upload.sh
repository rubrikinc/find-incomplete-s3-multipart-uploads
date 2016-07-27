for bucket in $(aws s3api list-buckets --query 'Buckets[*].{Name:Name}' --output text)
do 
    
    echo "$bucket:"
    
    region=$(aws s3api get-bucket-location --bucket $bucket --query 'LocationConstraint' --output text | awk '{sub(/None/,"eu-west-1")}; 1')
    parts=$(aws s3api list-multipart-uploads --bucket $bucket --region $region --query 'Uploads[*].{Key:Key,UploadId:UploadId}' --output text)

    if [ "$parts" != "None" ]; then
        IFS=$'\n'
        for part in $parts
        do
            keyname=$(echo $part | awk '{print $1}')
            upload_id=$(echo $part | awk '{print $2}')
            id_size=$(aws s3api list-parts --upload-id $upload_id --bucket $bucket --key $keyname | grep "Size" | egrep -o '[0-9]+' | awk '{ SUM += $1} END { print SUM }')
            echo "size: $id_size bytes"
            # uncomment below to delete instead of printing the size
            #aws s3api abort-multipart-upload --bucket --key $keyname --upload-id $upload_id
        done
        
    fi
done