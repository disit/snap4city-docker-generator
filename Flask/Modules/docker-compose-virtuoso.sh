services:
  virtuoso-new:
    container_name: virtuoso-new
    environment:
      DBA_PASSWORD: $#virtuoso-kb-pwd#$
      #DEFAULT_GRAPH: http://www.example.com/my-graph   -> already internal
      #SPARQL_UPDATE: "true"                            -> need to run 'GRANT SPARQL_UPDATE TO "SPARQL"';
      VIRT_Parameters_MaxDirtyBuffers: 130000
      VIRT_Parameters_NumberOfBuffers: 170000
      VIRT_Parameters_ServerThreads: 100
    image: openlink/virtuoso-opensource-7:7.2
    logging:
      driver: json-file
      options:
        max-file: '10'
        max-size: 100m
    #ports:                                             -> commented because conflict with original one
    #- published: 1111
    #  target: 1111
    #- published: 8890
    #  target: 8890
    restart: unless-stopped
    volumes:
    - virtuoso-new:/opt/virtuoso-opensource/database:rw
    - ./servicemap-conf-new:/root/servicemap:rw
volumes:
  virtuoso-new: {}