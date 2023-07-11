$graph:

- class: Workflow
  doc: Runs daops subsetting process
  id: daops
  requirements:
  - class: ScatterFeatureRequirement
  inputs:
    area:
      doc: Area
      label: Area
      type: string[]
    time:
      doc: Time
      label: Time
      type: string[]
    time_components:
      doc: Time Components
      label: Time Components
      type: string[]
    level:
      doc: Level
      label: Level
      type: string[]
    output_format:
      doc: Output Format
      label: Output Format
      type: string[]
    file_namer:
      doc: File Namer
      label: File Namer
      type: string[]
    output_dir:
      doc: Output dir
      label: Output dir
      type: string[]
    collection:
      doc: Collection
      label: Collection
      type: string[]  
  label: data-aware operations (daops)
  outputs:
  - id: wf_outputs
    outputSource:
    - step_1/results
    type:
      Directory[]

  steps:
    step_1:
      in:
        area: area
        time: time
        time_components: time_components
        level: level
        output_format: output_format
        file_namer: file_namer
        output_dir: output_dir
        collection: collection
      out:
      - results
      run: '#clt'
      scatter: [area, time, time_components, level, output_format, file_namer, output_dir, collection]
      scatterMethod: flat_crossproduct

- baseCommand: daops
  class: CommandLineTool

  id: clt

  arguments:
  - --area
  - valueFrom: $( inputs.area )
  - --time
  - valueFrom: ${ inputs.time }
  - --time-components
  - valueFrom: ${ inputs.time_components }
  - --levels
  - valueFrom: ${ inputs.levels }
  - --output-format
  - valueFrom: ${ inputs.output_format }
  - --file-namer
  - valueFrom: ${ inputs.file_namer }
  - --output-dir
  - valueFrom: ${ inputs.output_dir }
  - --collection
  - valueFrom: ${ inputs.collection }
  
  inputs:
    area:
      type: string
    time:
      type: string
    time_components:
      type: string 
    level:
      type: string
    output_format:
      type: string
    file_namer:
      type: string
    output_dir:
      type: string
    collection:
      type: string

  outputs:
    results:
      outputBinding:
        glob: .
      type: Directory
  requirements:
    EnvVarRequirement:
      envDef:
        PATH: /bin:/srv/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
    ResourceRequirement: {}
    InlineJavascriptRequirement: {}
    DockerRequirement:
      dockerPull: alaniwi/daops:latest
  #stderr: std.err
  #stdout: std.out

cwlVersion: v1.0

$namespaces:
  s: https://schema.org/
s:softwareVersion: 0.3.0
schemas:
- http://schema.org/version/9.0/schemaorg-current-http.rdf
