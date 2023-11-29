cwlVersion: v1.0
$namespaces:
  s: https://schema.org/
s:softwareVersion: 1.1.7
schemas:
  - http://schema.org/version/9.0/schemaorg-current-http.rdf

$graph:

  - class: Workflow
    id: daops
    label: daops
    doc: daops
    requirements:
      - class: ScatterFeatureRequirement

    inputs:
      time:
          doc: time
          type: string
      collection:
          doc: collection
          type: string
      file_namer:
          doc: file_namer
          type: string
      output_dir:
          doc: output_dir
          type: string

    outputs:
      - id: wf_outputs
        outputSource:
          - subset/results
        type: File

    steps:
      subset:
        run: "#clt"
        in:
            time: time
            collection: collection
            file_namer: file_namer
            output_dir: output_dir
        out: 
          - results

  - class: CommandLineTool
    id: clt
    requirements:
      InlineJavascriptRequirement: {}
      EnvVarRequirement:
        envDef:  
           ROOCS_CONFIG: /root/roocs.ini
#          PATH: /srv/conda/envs/env_crop/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
#          PYTHONPATH: /home/jovyan/ogc-eo-application-package-hands-on/water-bodies/command-line-tools/crop:/home/jovyan/water-bodies/command-line-tools/crop:/workspaces/vscode-binder/command-line-tools/crop
#          PROJ_LIB: /srv/conda/envs/env_crop/share/proj/
#      ResourceRequirement:
#        coresMax: 1
#        ramMax: 500Mb
    hints:
      DockerRequirement:
        dockerPull: agstephens/daops-kerchunk:v0.3
    baseCommand: ["daops", "subset"]

    arguments: []
    inputs:
      time:
        type: string
        inputBinding:
          prefix: --time
          position: 1
      file_namer:
        type: string
        inputBinding:
          prefix: --file-namer
          position: 2
      output_dir:
        type: string
        inputBinding:
          prefix: --output-dir
          position: 3
      collection:
        type: string
        inputBinding:
          position: 4
    outputs:
      results:
        outputBinding:
          glob: "./*.nc"
        type: File
