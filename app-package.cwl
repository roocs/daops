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
      area:
          doc: area
          type: string
      time:
          doc: time
          type: string
      time_components:
          doc: time_components
          type: string
      levels:
          doc: levels
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
            area: area
            time: time
            time_components: time_components
            levels: levels
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
#      ResourceRequirement:
#        coresMax: 1
#        ramMax: 500Mb
    hints:
      DockerRequirement:
        dockerPull: agstephens/daops-kerchunk:v0.4
    baseCommand: ["daops", "subset"]

    arguments: []
    inputs:
      area:
        type: string
        inputBinding:
          prefix: --area
          position: 1
      time:
        type: string
        inputBinding:
          prefix: --time
          position: 2
      time_components:
        type: string
        inputBinding:
          prefix: --time-components
          position: 3
      levels:
        type: string
        inputBinding:
          prefix: --levels
          position: 4
      file_namer:
        type: string
        inputBinding:
          prefix: --file-namer
          position: 5
      output_dir:
        type: string
        inputBinding:
          prefix: --output-dir
          position: 6
      collection:
        type: string
        inputBinding:
          position: 7
    outputs:
      results:
        outputBinding:
          glob: "./*.nc"
        type: File
